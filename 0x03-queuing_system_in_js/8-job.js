import kue from 'kue';

export function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  jobs.forEach((job) => {
    const jobInstance = queue.create('push_notification_code_3', job);

    jobInstance.on('enqueue', () => {
      console.log(`Notification job created: ${jobInstance.id}`);
    });

    jobInstance.on('complete', () => {
      console.log(`Notification job ${jobInstance.id} completed`);
    });

    jobInstance.on('failed', (err) => {
      console.log(`Notification job ${jobInstance.id} failed: ${err.message}`);
    });

    jobInstance.on('progress', (progress) => {
      console.log(`Notification job ${jobInstance.id} ${progress}% complete`);
    });

    jobInstance.save((err) => {
      if (err) {
        console.error(`Error saving job: ${err.message}`);
      }
    });
  });
}
