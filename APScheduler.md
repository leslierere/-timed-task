# Features
- You can add new jobs or remove old ones on the fly as you please.
- APScheduler is not a daemon or service itself, nor does it come with any command line tools. It is primarily meant to be run inside existing applications.

# Three built-in scheduling systems you can use
- Cron-style scheduling (with optional start/end times)
- Interval-based execution (runs jobs on even intervals, with optional start/end times)  
固定时间间隔执行，可选开始和结束程序时间
- One-off delayed execution (runs jobs once, on a set date/time)   
一次性的延时执行程序

# APScheduler has four kinds of components
- triggers
- job stores
- executors
- schedulers

## triggers
Each job has its own trigger which determines when the job should be run next.   
每个任务有自己的触发器
## job stores
Job stores house the scheduled jobs. The default job store simply keeps the jobs in memory, but others store them in various kinds of databases. A job’s data is serialized when it is saved to a persistent job store, and deserialized when it’s loaded back from it. Job stores (other than the default one) don’t keep the job data in memory, but act as middlemen for saving, loading, updating and searching jobs in the backend. Job stores must never be shared between schedulers.  
存储计划任务。默认的job stores将任务存储在内存，其他种类的job stores只是作为存储任务到其他后端（各种数据库）的媒介。job stores不能被schedulers共享
## executors
Handle the running of the jobs. They do this typically by submitting the designated callable in a job to a thread or process pool. When the job is done, the executor notifies the scheduler which then emits an appropriate event.  
执行任务，通过将job提交到线程或进程池实现。当任务完成，executor会通知scheduler，于是释放合适的事件（是释放该进程或线程的意思吗？）
## schedulers
Bind the rest together. You typically have only one scheduler running in your application. The application developer doesn’t normally deal with the job stores, executors or triggers directly. Instead, the scheduler provides the proper interface to handle all those. Configuring the job stores and executors is done through the scheduler, as is adding, modifying and removing jobs.
每个程序只应包含一个scheduler。我们通常不会直接处理job stores, executors，trigger，而是通过scheduler提供的接口实现。


# 选择正确的scheduler
- BlockingScheduler: use when the scheduler is the only thing running in your process  
当scheduler是程序中唯一需要运行的东西
- BackgroundScheduler: use when you’re not using any of the frameworks below, and want the scheduler to run in the background inside your application  
当没用下面几个框架时，并且想要scheduler在程序的后台运行
- AsyncIOScheduler: use if your application uses the asyncio module  
当程序为异步模式
- GeventScheduler: use if your application uses gevent  
- TornadoScheduler: use if you’re building a Tornado application  
- TwistedScheduler: use if you’re building a Twisted application  
- QtScheduler: use if you’re building a Qt application  

## 选择正确的job store
To pick the appropriate job store, you need to determine whether you need job persistence or not. If you always recreate your jobs at the start of your application, then you can probably go with the default (MemoryJobStore). But if you need your jobs to persist over scheduler restarts or application crashes, then your choice usually boils down to what tools are used in your programming environment. If, however, you are in the position to choose freely, then SQLAlchemyJobStore on a PostgreSQL backend is the recommended choice due to its strong data integrity protection.    
取决于你是否需要项目持续运行。如果总是在程序开始时重新创建任务，就可以使用默认的。如果
