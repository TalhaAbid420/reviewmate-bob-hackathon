const express = require('express');
const db = require('../db');

const router = express.Router();

// POST /tasks - create a task
// NOTE (intentional bug for demo): no validation on `title`.
// An empty string, missing field, or non-string value is accepted and stored as-is.
router.post('/', (req, res) => {
  const { title } = req.body;
  const task = db.createTask(title);
  res.status(201).json(task);
});

// GET /tasks/:id - fetch a task by id
router.get('/:id', (req, res) => {
  const task = db.getTaskById(req.params.id);
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }
  res.json(task);
});

// DELETE /tasks/:id - delete a task by id
// NOTE (intentional gap for demo): this endpoint has no test coverage.
router.delete('/:id', (req, res) => {
  const deleted = db.deleteTaskById(req.params.id);
  if (!deleted) {
    return res.status(404).json({ error: 'Task not found' });
  }
  res.status(204).send();
});

module.exports = router;
