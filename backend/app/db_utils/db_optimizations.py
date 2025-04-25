from typing import Any, Dict, List, Optional, Type, Union, TypeVar
from sqlalchemy.orm import Query, joinedload, selectinload
from sqlalchemy.ext.declarative import DeclarativeBase

T = TypeVar('T', bound=DeclarativeBase)

class QueryOptimizer:
    """
    A utility class for optimizing SQLAlchemy database queries by intelligently
    using joinedload and selectinload to reduce the number of database queries.
    """
    
    @staticmethod
    def optimize_single_object_query(model_class: Type[T], 
                                    query_params: Dict[str, Any],
                                    join_related_fields: Optional[List[str]] = None,
                                    select_related_fields: Optional[List[str]] = None,
                                    db_session=None) -> Optional[T]:
        """
        Optimizes a query for retrieving a single object by using joinedload and selectinload.
        
        Args:
            model_class: The SQLAlchemy model class to query
            query_params: Dictionary of query parameters to filter the object
            join_related_fields: List of field names for joinedload (OneToOne or ForeignKey relationships)
            select_related_fields: List of field names for selectinload (ManyToMany or reverse relationships)
            db_session: SQLAlchemy database session
            
        Returns:
            A single model instance or None if not found
        """
        query = db_session.query(model_class).filter_by(**query_params)
        
        if join_related_fields:
            for field in join_related_fields:
                query = query.options(joinedload(field))
            
        if select_related_fields:
            for field in select_related_fields:
                query = query.options(selectinload(field))
        
        return query.first()
    
    @staticmethod
    def optimize_queryset(query: Query,
                         join_related_fields: Optional[List[str]] = None,
                         select_related_fields: Optional[List[str]] = None) -> Query:
        """
        Optimizes an existing query by adding joinedload and selectinload.
        
        Args:
            query: The existing SQLAlchemy query to optimize
            join_related_fields: List of field names for joinedload
            select_related_fields: List of field names for selectinload
            
        Returns:
            An optimized query
        """
        if join_related_fields:
            for field in join_related_fields:
                query = query.options(joinedload(field))
            
        if select_related_fields:
            for field in select_related_fields:
                query = query.options(selectinload(field))
                
        return query


class OptimizedQuerySetMixin:
    """
    A mixin for FastAPI dependency injectors that adds methods for optimizing queries with
    joinedload and selectinload.
    """
    
    join_related_fields: List[str] = []
    select_related_fields: List[str] = []
    
    def get_query(self, db_session):
        """
        Get the base query for the model.
        """
        query = db_session.query(self.model)
        return self._optimize_query(query)
    
    def _optimize_query(self, query):
        """
        Apply joinedload and selectinload optimizations to a query.
        """
        # Apply joinedload if fields are defined
        if self.join_related_fields:
            for field in self.join_related_fields:
                query = query.options(joinedload(field))
        
        # Apply selectinload for related fields
        if self.select_related_fields:
            for field in self.select_related_fields:
                query = query.options(selectinload(field))
        
        return query


# Common optimization patterns for the UserProfile model and related models
def get_optimized_user_profile(user_id: Union[str, int], db_session) -> Optional[Any]:
    """
    Get a UserProfile with all commonly needed related objects prefetched.
    
    Args:
        user_id: The primary key of the user
        db_session: SQLAlchemy database session
        
    Returns:
        UserProfile object with optimized queries or None if not found
    """
    from app.models import UserProfile
    
    return QueryOptimizer.optimize_single_object_query(
        model_class=UserProfile,
        query_params={'user_id': user_id},
        join_related_fields=['user'],
        db_session=db_session
    )
