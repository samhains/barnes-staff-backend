/**
 * Tag.js
 *
 */

module.exports = {

  attributes: {
    name: {
      type: 'string',
      required: true,
    },
    confidence: {
      type: 'float',
    },
    service: {
      model: 'service',
      required: true,
    },
    artwork: {
      model: 'artwork',
      required: true,
    },
  },
};

