const request = require('supertest');
const app = require('../src/app');
const db = require('../src/db');

beforeEach(() => {
  db.reset();
});

describe('POST /tasks', () => {
  it('creates a new task and returns it', async () => {
    const res = await request(app).post('/tasks').send({ title: 'Write report' });
    expect(res.status).toBe(201);
    expect(res.body).toMatchObject({ title: 'Write report', done: false });
    expect(res.body.id).toBeDefined();
  });
});

describe('GET /tasks/:id', () => {
  it('returns the task when it exists', async () => {
    const created = await request(app).post('/tasks').send({ title: 'Read book' });
    const res = await request(app).get(`/tasks/${created.body.id}`);
    expect(res.status).toBe(200);
    expect(res.body.title).toBe('Read book');
  });

  it('returns 404 when the task does not exist', async () => {
    const res = await request(app).get('/tasks/9999');
    expect(res.status).toBe(404);
  });
});

// NOTE: DELETE /tasks/:id has no tests here.
// This gap is intentional - it's what the test-coverage subagent should catch.
