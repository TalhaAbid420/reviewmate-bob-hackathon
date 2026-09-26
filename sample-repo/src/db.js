// Simple in-memory store - no real database needed for this demo
let tasks = [];
let nextId = 1;

function createTask(title) {
  const task = { id: nextId++, title, done: false };
  tasks.push(task);
  return task;
}

function getTaskById(id) {
  return tasks.find((t) => t.id === Number(id));
}

function deleteTaskById(id) {
  const index = tasks.findIndex((t) => t.id === Number(id));
  if (index === -1) return false;
  tasks.splice(index, 1);
  return true;
}

function reset() {
  tasks = [];
  nextId = 1;
}

module.exports = { createTask, getTaskById, deleteTaskById, reset };
