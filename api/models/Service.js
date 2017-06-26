/**
 * Service.js
 *
 */

module.exports = {

  attributes: {
    name: {
      type: 'string',
      required: true,
    },
    tags: {
      collection: 'tag',
      via: 'service',
    },
  },

};

