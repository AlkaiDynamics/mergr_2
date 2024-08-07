## frontend/src/components/ProjectManagement.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProjectManagement = () => {
  const [projects, setProjects] = useState([]);
  const [projectName, setProjectName] = useState('');
  const [projectDescription, setProjectDescription] = useState('');
  const [members, setMembers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [taskName, setTaskName] = useState('');
  const [taskDescription, setTaskDescription] = useState('');
  const [assignedTo, setAssignedTo] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [status, setStatus] = useState('Pending');

  useEffect(() => {
    // Fetch initial project data
    axios.get('/projects/')
      .then(response => {
        setProjects(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the projects!', error);
      });
  }, []);

  const handleCreateProject = () => {
    const newProject = {
      name: projectName,
      description: projectDescription,
      members: members.split(',').map(member => member.trim())
    };

    axios.post('/projects/', newProject)
      .then(response => {
        setProjects([...projects, response.data]);
        setProjectName('');
        setProjectDescription('');
        setMembers('');
        alert('Project created successfully!');
      })
      .catch(error => {
        console.error('There was an error creating the project!', error);
      });
  };

  const handleCreateTask = (projectId) => {
    const newTask = {
      name: taskName,
      description: taskDescription,
      assigned_to: assignedTo,
      due_date: dueDate,
      status: status,
      project: projectId
    };

    axios.post(`/projects/${projectId}/tasks/`, newTask)
      .then(response => {
        setTasks([...tasks, response.data]);
        setTaskName('');
        setTaskDescription('');
        setAssignedTo('');
        setDueDate('');
        setStatus('Pending');
        alert('Task created successfully!');
      })
      .catch(error => {
        console.error('There was an error creating the task!', error);
      });
  };

  return (
    <div className="project-management-container">
      <h2>Project Management</h2>
      <div className="create-project">
        <h3>Create Project</h3>
        <div className="form-group">
          <label htmlFor="projectName">Project Name:</label>
          <input
            type="text"
            id="projectName"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="projectDescription">Project Description:</label>
          <textarea
            id="projectDescription"
            value={projectDescription}
            onChange={(e) => setProjectDescription(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="members">Members (comma separated):</label>
          <input
            type="text"
            id="members"
            value={members}
            onChange={(e) => setMembers(e.target.value)}
          />
        </div>
        <button onClick={handleCreateProject}>Create Project</button>
      </div>
      <div className="project-list">
        <h3>Projects</h3>
        {projects.map((project) => (
          <div key={project.id} className="project-item">
            <h4>{project.name}</h4>
            <p>{project.description}</p>
            <h5>Members:</h5>
            <ul>
              {project.members.map((member, index) => (
                <li key={index}>{member.username}</li>
              ))}
            </ul>
            <h5>Tasks:</h5>
            <ul>
              {project.tasks.map((task, index) => (
                <li key={index}>{task.name} - {task.status}</li>
              ))}
            </ul>
            <div className="create-task">
              <h5>Create Task</h5>
              <div className="form-group">
                <label htmlFor={`taskName-${project.id}`}>Task Name:</label>
                <input
                  type="text"
                  id={`taskName-${project.id}`}
                  value={taskName}
                  onChange={(e) => setTaskName(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor={`taskDescription-${project.id}`}>Task Description:</label>
                <textarea
                  id={`taskDescription-${project.id}`}
                  value={taskDescription}
                  onChange={(e) => setTaskDescription(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor={`assignedTo-${project.id}`}>Assigned To:</label>
                <input
                  type="text"
                  id={`assignedTo-${project.id}`}
                  value={assignedTo}
                  onChange={(e) => setAssignedTo(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor={`dueDate-${project.id}`}>Due Date:</label>
                <input
                  type="date"
                  id={`dueDate-${project.id}`}
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor={`status-${project.id}`}>Status:</label>
                <select
                  id={`status-${project.id}`}
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                >
                  <option value="Pending">Pending</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>
              <button onClick={() => handleCreateTask(project.id)}>Create Task</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProjectManagement;
