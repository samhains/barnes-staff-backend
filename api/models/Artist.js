/**
 * Artist.js
 *
 */

module.exports = {

  attributes: {
    name: {
      type: 'string',
      required: true,
    },
    artworks: {
      collection: 'artwork',
      via: 'artist',
    },
  },
};

