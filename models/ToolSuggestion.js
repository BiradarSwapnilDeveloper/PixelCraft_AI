const mongoose = require('mongoose');

const ToolSuggestionSchema = new mongoose.Schema({
  toolName: {
    type: String,
    required: true,
    trim: true,
    maxlength: 150
  },
  description: {
    type: String,
    required: true,
    trim: true,
    maxlength: 2000
  },
  email: {
    type: String,
    trim: true,
    default: '',
    maxlength: 150
  },
  searchQuery: {
    type: String,
    trim: true,
    default: '',
    maxlength: 150
  },
  clientIp: {
    type: String,
    default: 'unknown'
  },
  userAgent: {
    type: String,
    default: 'unknown'
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.models.ToolSuggestion || mongoose.model('ToolSuggestion', ToolSuggestionSchema);
