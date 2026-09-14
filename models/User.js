const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  googleId: {
    type: String,
    required: true,
    unique: true
  },
  name: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  avatar: {
    type: String
  },
  toolsUsedCount: {
    type: Number,
    default: 0
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  lastLogin: {
    type: Date,
    default: Date.now
  },
  loginCount: {
    type: Number,
    default: 0
  },
  isBanned: {
    type: Boolean,
    default: false
  },
  banUntil: {
    type: Date,
    default: null
  },
  banReason: {
    type: String,
    default: ''
  },
  toolUsageHistory: [{
    toolName: String,
    usedAt: { type: Date, default: Date.now },
    durationSeconds: Number
  }]
});

module.exports = mongoose.model('User', UserSchema);
