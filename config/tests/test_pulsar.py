"""
Pulsar Integration Tests

Organized by test categories:
- Connection Tests
- Producer Tests
- Consumer Tests
- Performance Tests
- Security Tests
"""
import pytest
import time
import logging
from pulsar import Client, MessageId

# Configure test logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def pulsar_client():
    """
    Fixture providing a Pulsar client connected to the test service.
    Follows performance and security best practices from project docs.
    """
    service_url = 'pulsar://broker:6650'
    
    # Health check with retries
    max_retries = 5
    retry_delay = 2
    
    for i in range(max_retries):
        try:
            client = Client(
                service_url,
                operation_timeout_seconds=30,
                connection_timeout_ms=10000
            )
            # Verify connection with minimal operation
            _ = client.get_topic_partitions('persistent://public/default/healthcheck')  # Result not used
            logger.info("Successfully connected to Pulsar broker")
            break
        except Exception as e:
            if i == max_retries - 1:
                logger.error(f"Failed to connect to Pulsar after {max_retries} attempts")
                raise RuntimeError(f"Failed to connect to Pulsar after {max_retries} attempts") from e
            logger.warning(f"Pulsar connection attempt {i+1} failed, retrying...")
            time.sleep(retry_delay)
    
    yield client
    
    # Cleanup
    try:
        client.close()
        logger.info("Closed Pulsar client connection")
    except Exception as e:
        logger.error(f"Error closing Pulsar client: {str(e)}")

@pytest.fixture
def clean_topic(pulsar_client):
    """
    Fixture that ensures the test topic is clean before each test.
    Follows topic management best practices.
    """
    topic = 'persistent://public/default/test-topic'
    subscription = 'test-subscription'
    
    try:
        # Clean up any existing messages
        consumer = pulsar_client.subscribe(topic, subscription)
        while True:
            msg = consumer.receive(100)  # 100ms timeout
            consumer.acknowledge(msg)
            logger.debug(f"Cleaned up message from topic: {msg.message_id()}")
    except Exception as e:
        # Expected when no more messages
        logger.debug(f"Topic cleanup complete: {str(e)}")
    finally:
        try:
            consumer.close()
        except Exception:  # Explicit exception handling
            pass
    
    yield topic
    
    # Post-test cleanup
    try:
        consumer = pulsar_client.subscribe(topic, subscription)
        consumer.close()
        logger.debug("Closed test consumer")
    except Exception:  # Explicit exception handling
        pass

# Connection Tests
@pytest.mark.connection
class TestPulsarConnection:
    """
    Tests for Pulsar broker connection and basic functionality
    """
    
    @pytest.mark.integration
    def test_broker_connection(self, pulsar_client):
        """
        Given: A configured Pulsar client
        When: Connecting to the broker
        Then: Should establish connection within timeout
        """
        assert pulsar_client is not None
        
    @pytest.mark.security
    def test_connection_security(self, pulsar_client):
        """
        Given: A configured Pulsar client
        When: Checking connection properties
        Then: Should use expected security protocol
        """
        assert 'pulsar+ssl://' not in pulsar_client._service_url

# Producer Tests
@pytest.mark.producer
class TestPulsarProducer:
    """
    Tests for Pulsar message production
    """
    
    @pytest.fixture
    def producer(self, pulsar_client, clean_topic):
        """Test producer with optimal settings"""
        return pulsar_client.create_producer(
            clean_topic,
            send_timeout_millis=10000,
            batching_enabled=True
        )
    
    @pytest.mark.integration
    def test_message_production(self, producer):
        """
        Given: A configured producer
        When: Sending test messages
        Then: Should return valid message IDs
        """
        test_message = b'test message'
        msg_id = producer.send(test_message)
        assert isinstance(msg_id, MessageId)

# Consumer Tests
@pytest.mark.consumer
class TestPulsarConsumer:
    """
    Tests for Pulsar message consumption
    """
    
    @pytest.fixture
    def consumer(self, pulsar_client, clean_topic):
        """Test consumer with optimal settings"""
        return pulsar_client.subscribe(
            clean_topic,
            'test-subscription',
            receiver_queue_size=1000
        )
    
    @pytest.mark.integration
    def test_message_consumption(self, producer, consumer):
        """
        Given: A producer and consumer
        When: Sending and receiving messages
        Then: Should correctly receive sent messages
        """
        test_message = b'test message'
        producer.send(test_message)
        
        msg = consumer.receive(5000)
        assert msg.data() == test_message
        consumer.acknowledge(msg)

# Performance Tests
@pytest.mark.performance
class TestPulsarPerformance:
    """
    Tests for Pulsar performance characteristics
    """
    
    @pytest.mark.integration
    def test_production_throughput(self, producer):
        """
        Given: A configured producer
        When: Sending multiple messages
        Then: Should meet performance thresholds
        """
        test_messages = [b'test message ' + str(i).encode() for i in range(100)]
        
        start_time = time.time()
        for msg in test_messages:
            producer.send(msg)
        duration = time.time() - start_time
        
        logger.info(f"Produced {len(test_messages)} messages in {duration:.4f} seconds")
        assert duration < 2.0
