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
    default: function() {
      // If legalHold is true at creation, do not set expiresAt (exempt from TTL)
      return this.legalHold ? null : new Date(Date.now() + 180 * 24 * 60 * 60 * 1000);
    }
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

// Enforce exemption in pre-save: if legalHold is true, expiresAt must be null/unset
TrapLogSchema.pre('save', function(next) {
  if (this.legalHold) {
    this.expiresAt = null;
  }
  next();
});

// Safe TTL index on expiresAt (MongoDB TTL ignores missing or null dates)
// Added partialFilterExpression: only index documents where legalHold is NOT true
TrapLogSchema.index(
  { expiresAt: 1 },
  {
    expireAfterSeconds: 0,
    background: true,
    partialFilterExpression: { legalHold: { $ne: true } }
  }
);

module.exports = mongoose.model('TrapLog', TrapLogSchema);
