import kue from 'kue';
import { createPushNotificationsJobs } from './8-job.js'; // Adjust path as necessary
import { expect } from 'chai';

describe('createPushNotificationsJobs', function() {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.exit();
    const jobs = queue.testMode.jobs;
    jobs.forEach((job) => {
      job.remove();
    });
  });

  it('should create jobs in the queue', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    const queuedJobs = queue.testMode.jobs;
    expect(queuedJobs).to.have.lengthOf(2);

    jobs.forEach((jobData, index) => {
      const job = queuedJobs[index];
      expect(job).to.have.property('type', 'push_notification_code_3');
      expect(job.data).to.deep.equal(jobData);
    });
  });

  it('should handle job completion', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);
    const job = queue.testMode.jobs[0];

    job.on('complete', () => {
      expect(job._events.complete).to.be.an('array').that.has.lengthOf(2);
      expect(job._events.complete[0]).to.be.a('Function');
      done();
    });

    job.emit('complete');
  });

  it('should handle job failure', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    const job = queue.testMode.jobs[0];

    job.on('failed', (error) => {
      expect(error).to.be.an('error');
      done();
    });

    job.emit('failed', new Error('Simulated failure'));
  });

  it('should handle job progress', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    const job = queue.testMode.jobs[0];

    job.on('progress', (progress) => {
      expect(progress).to.be.a('number');
      done();
    });

    job.emit('progress', 50);
  });
});
