/**
 * Artwork.js
 *
 */

module.exports = {
  attributes: {
    name: {
      type: 'string',
      required: true,
    },
    url: {
      name: { type: 'string' },
      required: true,
    },
    artist: {
      model: 'artist',
      required: true,
    },
    tags: {
      collection: 'tag',
      via: 'artwork',
    },
  },
};

