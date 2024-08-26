import express from 'express';
import redis from 'redis';
import kue from 'kue';
import util from 'util';

const client = redis.createClient();
const getAsync = util.promisify(client.get).bind(client);
const setAsync = util.promisify(client.set).bind(client);
const queue = kue.createQueue();
const INITIAL_SEATS = 50;
let reservationEnabled = true;

const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats, 10) : 0;
};

reserveSeat(INITIAL_SEATS);

const app = express();
const port = 1245;

app.get('/available_seats', async (_, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

app.get('/reserve_seat', (_, res) => {
  if (!reservationEnabled) {
    return res.status(400).json({ status: 'Reservations are blocked' });
  }
  const job = queue.create('reserve_seat', {}).save((err) => {
    if (err) {
      return res.status(500).json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (_, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }

  queue.process('reserve_seat', async (_, done) => {
    try {
      const availableSeats = await getCurrentAvailableSeats();
      if (availableSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }

      await reserveSeat(availableSeats - 1);
      done();
    } catch (error) {
      done(error);
    }
  });

  res.json({ status: 'Queue processing' });
});


app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
