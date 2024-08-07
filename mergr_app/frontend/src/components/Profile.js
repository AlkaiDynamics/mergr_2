## frontend/src/components/Profile.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Profile = () => {
  const [profile, setProfile] = useState({
    user: {
      id: '',
      username: '',
      email: ''
    },
    skills: [],
    interests: [],
    bio: ''
  });
  const [skills, setSkills] = useState('');
  const [interests, setInterests] = useState('');
  const [bio, setBio] = useState('');

  useEffect(() => {
    // Fetch user profile data
    axios.get('/profiles/')
      .then(response => {
        setProfile(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the profile!', error);
      });
  }, []);

  const handleUpdateProfile = () => {
    const updatedProfile = {
      user: profile.user,
      skills: skills.split(',').map(skill => skill.trim()),
      interests: interests.split(',').map(interest => interest.trim()),
      bio: bio
    };

    axios.put(`/profiles/${profile.id}/`, updatedProfile)
      .then(response => {
        setProfile(response.data);
        alert('Profile updated successfully!');
      })
      .catch(error => {
        console.error('There was an error updating the profile!', error);
      });
  };

  return (
    <div className="profile-container">
      <h2>User Profile</h2>
      <div className="profile-details">
        <p><strong>Username:</strong> {profile.user.username}</p>
        <p><strong>Email:</strong> {profile.user.email}</p>
        <p><strong>Skills:</strong> {profile.skills.join(', ')}</p>
        <p><strong>Interests:</strong> {profile.interests.join(', ')}</p>
        <p><strong>Bio:</strong> {profile.bio}</p>
      </div>
      <div className="profile-edit">
        <h3>Edit Profile</h3>
        <div className="form-group">
          <label htmlFor="skills">Skills (comma separated):</label>
          <input
            type="text"
            id="skills"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="interests">Interests (comma separated):</label>
          <input
            type="text"
            id="interests"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="bio">Bio:</label>
          <textarea
            id="bio"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
          />
        </div>
        <button onClick={handleUpdateProfile}>Update Profile</button>
      </div>
    </div>
  );
};

export default Profile;
