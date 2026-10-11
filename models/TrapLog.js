const mongoose = require('mongoose');

const TrapLogSchema = new mongoose.Schema({
  tokenId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Honeytoken',
    required: true
  },
  ipAddress: {
    type: String,
    required: true
  },
  location: {
    type: String,
    default: 'Unknown'
  },
  isp: {
    type: String,
    default: 'Unknown'
  },
  userAgent: {
    type: String,
    default: 'Unknown'
  },
  method: {
    type: String
  },
  endpoint: {
    type: String
  },
  payloadSent: {
    type: mongoose.Schema.Types.Mixed,
    default: {}
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
  expiresAt: {
    type: Date,
    default: () => new Date(Date.now() + 180 * 24 * 60 * 60 * 1000)
  },
  legalHold: {
    type: Boolean,
    default: false
  },
  legalHoldReason: {
    type: String,
    default: null
  },
  legalHoldPlacedAt: {
    type: Date,
    default: null
  },
  legalHoldPlacedBy: {
    type: String,
    default: null
  }
});

// Safe TTL index on expiresAt (MongoDB TTL ignores missing or null dates)
TrapLogSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0, background: true });

module.exports = mongoose.model('TrapLog', TrapLogSchema);
