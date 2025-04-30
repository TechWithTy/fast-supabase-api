1. Best Practices


Celery recommends you put all rate limited tasks in their own queue and to use the rate_limit kwarg for the shared task. If you have multiple API calls you should split those up into their own rate limited tasks that go into its own queue as well. Is there a reason you didn't use the built in rate limit?

    Prefer RabbitMQ or Redis
as broker (never use a relational database as production broker).
Do not use complex objects in task as parameters. E.g.: Avoid Django model objects:
Do not wait for other tasks inside a task.
Prefer idempotent tasks:
Prefer atomic tasks:
Retry when possible. But make sure tasks are idempotent and atomic before doing so. (Retrying)
Set retry_limit to avoid broken tasks to keep retrying forever.
Exponentially backoff if things look like they are not going to get fixed soon. Throw in a random factor to avoid cluttering services:
Use autoretry_for
to reduce the boilerplate code for retrying tasks.
Use retry_backoff
to reduce the boilerplate code when doing exponention backoff.
For tasks that require high level of reliability, use acks_late in combination with retry. Again, make sure tasks are idempotent and atomic. (Should I use retry or acks_late?)
Set hard and soft time limits. Recover gracefully if things take longer than expected:
Use multiple queues to have more control over throughput and make things more scalable. (Routing Tasks)
Extend the base task class to define default behaviour. (Custom Task Classes)
Use canvas features to control task flows and deal with concurrency. (Canvas: Designing Work-flows)

2. Monitoring & Tests

    Log as much as possible. Use get_task_logger to automatically get the task name and unique id as part of the logs.
    In case of failure, make sure stack traces get logged and people get notified (services like Sentry

are a good idea).
Monitor activity using Flower. (Flower: Real-time Celery web-monitor)

    Use task_always_eager to test your tasks are geting called.

3. Resources to check

    Celery: an overview of the architecture and how it works

by Vinta.
Celery in the wild: tips and tricks to run async tasks in the real world
by Vinta.
Celery Best Practices
by Balthazar Rouberol.
Dealing with resource-consuming tasks on Celery
by Vinta.
Tips and Best Practices
from the official documentation.
Task Queues
by Full Stack Python Flower: Real-time Celery web-monitor
from the official documentation.
Celery Best Practices: practical approach
by Adil.
3 GOTCHAS FOR CELERY
from Wiredcraft.
CELERY - BEST PRACTICES
by Deni Bertovic.
Hacker News thread on the above post.
[video] Painting on a Distributed Canvas: An Advanced Guide to Celery Workflows
by David Gouldin.
Celery in Production
by Dan Poirier from Caktus Group.
[video] Implementing Celery, Lessons Learned
by Michael Robellard.
[video] Advanced Celery
by Ask Solem Hoel.