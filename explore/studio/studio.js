(function () {
  'use strict';

  var CAROUSEL_W = 1080;
  var CAROUSEL_H = 1350;
  var GRID_W = 1080;
  var GRID_H = 1440;
  var STORY_W = 1080;
  var STORY_H = 1920;

  var PLACEHOLDER = '../assets/ocean-calling.jpg';
  var LOGO_SRC = '../assets/logo.png';
  var EXPORT_BASE = '../assets/studio/exports/';

  var MEME_PACK = [
    {
      title: 'Ocean call popup — phone ringing',
      items: [
        { file: 'lanka-popup-sleeve-story-9x16.mp4', label: 'Sleeve · story 9:16', type: 'video' },
        { file: 'lanka-popup-sleeve-feed-3x4.mp4', label: 'Sleeve · feed 3:4', type: 'video' },
        { file: 'lanka-popup-quiet-story-9x16.mp4', label: 'Quiet · story 9:16', type: 'video' },
        { file: 'lanka-popup-quiet-feed-3x4.mp4', label: 'Quiet · feed 3:4', type: 'video' },
      ],
    },
    {
      title: 'Opening row — upload Post 01 first',
      items: [
        { file: 'lanka-opening-grid-post-01.png', label: 'Post 01 · blue logo · right' },
        { file: 'lanka-opening-grid-post-02.png', label: 'Post 02 · sunset · center' },
        { file: 'lanka-opening-grid-post-03.png', label: 'Post 03 · red logo · left · last' },
        { file: 'lanka-opening-sunset-feed-3x4.png', label: 'Sunset solo' },
        { file: 'lanka-opening-sunset-story-9x16.png', label: 'Story 9:16' },
      ],
    },
    {
      title: 'Logo posts — static + animated',
      items: [
        { file: 'lanka-logo-red-3x4.png', label: 'Red logo · still' },
        { file: 'lanka-logo-red-animated.mp4', label: 'Red logo · animated', type: 'video' },
        { file: 'lanka-logo-blue-3x4.png', label: 'Blue logo · still' },
        { file: 'lanka-logo-blue-animated.mp4', label: 'Blue logo · animated', type: 'video' },
      ],
    },
    {
      title: 'Courses grid — upload Post 01 first',
      items: [
        { file: 'lanka-course-grid-post-01.png', label: 'Post 01 · Wave 2 · first' },
        { file: 'lanka-course-grid-post-02.png', label: 'Post 02 · Wave 1' },
        { file: 'lanka-course-grid-post-03.png', label: 'Post 03 · Discover · last' },
        { file: 'lanka-course-discover-3x4.png', label: 'Discover solo' },
        { file: 'lanka-course-wave1-3x4.png', label: 'Wave 1 solo' },
        { file: 'lanka-course-wave2-3x4.png', label: 'Wave 2 solo' },
      ],
    },
    {
      title: 'SpongeBob opening video',
      items: [
        { file: 'lanka-spongebob-opening-overlay.mp4', label: 'Story · text overlay', type: 'video' },
      ],
    },
    {
      title: 'SpongeBob grid — upload Post 01 first',
      items: [
        { file: 'lanka-spongebob-grid-post-01.png', label: 'Post 01 · right · first' },
        { file: 'lanka-spongebob-grid-post-02.png', label: 'Post 02 · center' },
        { file: 'lanka-spongebob-grid-post-03.png', label: 'Post 03 · left · last' },
      ],
    },
    {
      title: 'Scary movie grid — upload Post 01 first',
      items: [
        { file: 'lanka-scary-grid-post-01.png', label: 'Post 01 · right · first' },
        { file: 'lanka-scary-grid-post-02.png', label: 'Post 02 · center' },
        { file: 'lanka-scary-grid-post-03.png', label: 'Post 03 · left · last' },
      ],
    },
    {
      title: 'Meme grid — upload Post 01 first',
      items: [
        { file: 'lanka-meme-grid-post-01.png', label: 'Post 01 · first' },
        { file: 'lanka-meme-grid-post-02.png', label: 'Post 02' },
        { file: 'lanka-meme-grid-post-03.png', label: 'Post 03' },
        { file: 'lanka-meme-grid-post-04.png', label: 'Post 04' },
        { file: 'lanka-meme-grid-post-05.png', label: 'Post 05' },
        { file: 'lanka-meme-grid-post-06.png', label: 'Post 06 · last' },
      ],
    },
  ];
  var COPY = {
    headline: 'Breathe less. See more.',
    subline: 'Unawatuna · Nov–Apr',
    cta: 'Get in touch',
    kicker: 'Lanka Freediving',
    quote: "Can't talk rn.\nThe ocean is calling.",
  };

  var LAYOUTS = {
    carousel: [
      { id: 'pano-3', name: 'Panorama 3', detail: '3 slides · 4:5', frames: 3, type: 'pano' },
      { id: 'pano-5', name: 'Panorama 5', detail: '5 slides · 4:5', frames: 5, type: 'pano' },
      { id: 'type-photo-type', name: 'Type · Photo · Type', detail: '3 slides · 4:5', frames: 3, type: 'tpt' },
      { id: 'quote-run', name: 'Quote run', detail: '5 slides · 4:5', frames: 5, type: 'quote' },
    ],
    grid: [
      { id: 'grid-6', name: 'Grid 6', detail: '3×2 · 3:4 tiles', frames: 6, cols: 3, rows: 2, type: 'grid' },
      { id: 'grid-9', name: 'Grid 9', detail: '3×3 · 3:4 tiles', frames: 9, cols: 3, rows: 3, type: 'grid' },
    ],
    story: [
      { id: 'story-photo', name: 'Photo + caption', detail: '9:16', frames: 1, type: 'story-photo' },
      { id: 'story-type', name: 'Type only', detail: '9:16', frames: 1, type: 'story-type' },
      { id: 'story-logo', name: 'Logo stamp', detail: '9:16', frames: 1, type: 'story-logo' },
    ],
  };

  var DB_NAME = 'lanka-studio-v1';
  var DB_VERSION = 1;

  var state = {
    style: 'sleeve',
    photos: [],
    layout: null,
    zoom: 100,
    panX: 0,
    panY: 0,
    headline: COPY.headline,
    subline: COPY.subline,
    showGuides: true,
    logo: null,
  };

  var els = {};

  function $(id) {
    return document.getElementById(id);
  }

  function tokens(style) {
    if (style === 'sleeve') {
      return {
        pairs: [
          { bg: '#D94F2A', fg: '#F0C419' },
          { bg: '#F0C419', fg: '#D94F2A' },
          { bg: '#F5EDE0', fg: '#1A1A1A' },
          { bg: '#1A1A1A', fg: '#F5EDE0' },
        ],
        border: 16,
      };
    }
    return {
      pairs: [
        { bg: '#F5EDE0', fg: '#1A1A1A' },
        { bg: '#F0C419', fg: '#1A1A1A' },
        { bg: '#1A1A1A', fg: '#F5EDE0' },
      ],
      border: 8,
    };
  }

  function openDB() {
    return new Promise(function (resolve, reject) {
      var req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = function () {
        var db = req.result;
        if (!db.objectStoreNames.contains('photos')) {
          db.createObjectStore('photos', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('prefs')) {
          db.createObjectStore('prefs', { keyPath: 'key' });
        }
      };
      req.onsuccess = function () { resolve(req.result); };
      req.onerror = function () { reject(req.error); };
    });
  }

  function dbPut(store, value) {
    return openDB().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, 'readwrite');
        tx.objectStore(store).put(value);
        tx.oncomplete = function () { resolve(); };
        tx.onerror = function () { reject(tx.error); };
      });
    });
  }

  function dbGetAll(store) {
    return openDB().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, 'readonly');
        var req = tx.objectStore(store).getAll();
        req.onsuccess = function () { resolve(req.result || []); };
        req.onerror = function () { reject(req.error); };
      });
    });
  }

  function dbDelete(store, key) {
    return openDB().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, 'readwrite');
        tx.objectStore(store).delete(key);
        tx.oncomplete = function () { resolve(); };
        tx.onerror = function () { reject(tx.error); };
      });
    });
  }

  function loadImage(src) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = function () { resolve(img); };
      img.onerror = reject;
      img.src = src;
    });
  }

  function blobToDataUrl(blob) {
    return new Promise(function (resolve, reject) {
      var reader = new FileReader();
      reader.onload = function () { resolve(reader.result); };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }

  function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
    var words = text.split(/\s+/);
    var line = '';
    var cy = y;
    for (var i = 0; i < words.length; i++) {
      var test = line ? line + ' ' + words[i] : words[i];
      if (ctx.measureText(test).width > maxWidth && line) {
        ctx.fillText(line, x, cy);
        line = words[i];
        cy += lineHeight;
      } else {
        line = test;
      }
    }
    if (line) ctx.fillText(line, x, cy);
    return cy;
  }

  function wrapTextCenter(ctx, text, x, y, maxWidth, lineHeight) {
    var lines = [];
    var words = text.split(/\s+/);
    var line = '';
    for (var i = 0; i < words.length; i++) {
      var test = line ? line + ' ' + words[i] : words[i];
      if (ctx.measureText(test).width > maxWidth && line) {
        lines.push(line);
        line = words[i];
      } else {
        line = test;
      }
    }
    if (line) lines.push(line);
    var cy = y;
    lines.forEach(function (ln) {
      ctx.fillText(ln, x, cy);
      cy += lineHeight;
    });
  }

  function drawCoverImage(ctx, img, dx, dy, dw, dh, zoom, panX, panY) {
    if (!img || !img.width) return;
    var z = zoom / 100;
    var scale = Math.max(dw / img.width, dh / img.height) * z;
    var sw = dw / scale;
    var sh = dh / scale;
    var cx = img.width / 2 + (panX / 100) * img.width * 0.45;
    var cy = img.height / 2 + (panY / 100) * img.height * 0.45;
    var sx = Math.max(0, Math.min(img.width - sw, cx - sw / 2));
    var sy = Math.max(0, Math.min(img.height - sh, cy - sh / 2));
    ctx.drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh);
  }

  function drawQuietWave(ctx, x, y, w, h, color) {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = Math.max(4, w * 0.008);
    ctx.lineCap = 'round';
    ctx.beginPath();
    var mid = y + h * 0.85;
    ctx.moveTo(x, mid);
    var steps = 6;
    for (var i = 1; i <= steps; i++) {
      var px = x + (w / steps) * i;
      var py = mid + (i % 2 === 0 ? -h * 0.04 : h * 0.04);
      ctx.lineTo(px, py);
    }
    ctx.stroke();
    ctx.restore();
  }

  function drawTypeCard(ctx, x, y, w, h, style, tok, headline, subline, pairIndex, opts) {
    opts = opts || {};
    var pair = tok.pairs[pairIndex % tok.pairs.length];
    ctx.fillStyle = pair.bg;
    ctx.fillRect(x, y, w, h);

    if (style === 'sleeve') {
      ctx.strokeStyle = pair.fg;
      ctx.lineWidth = tok.border;
      ctx.strokeRect(x + tok.border / 2, y + tok.border / 2, w - tok.border, h - tok.border);
    } else {
      ctx.strokeStyle = pair.fg;
      ctx.lineWidth = tok.border;
      ctx.strokeRect(x + tok.border, y + tok.border, w - tok.border * 2, h - tok.border * 2);
      drawQuietWave(ctx, x, y, w, h, pair.fg);
    }

    ctx.fillStyle = pair.fg;
    var titleSize = Math.round(w * 0.088);
    ctx.font = titleSize + 'px "Bowlby One SC", serif';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    var pad = w * 0.09;
    var titleY = opts.center ? h * 0.38 : h * 0.14;
    if (opts.center) {
      ctx.textAlign = 'center';
      wrapTextCenter(ctx, (headline || COPY.headline).toUpperCase(), x + w / 2, titleY, w * 0.82, titleSize * 1.15);
    } else {
      wrapText(ctx, (headline || COPY.headline).toUpperCase(), x + pad, titleY, w - pad * 2, titleSize * 1.12);
    }

    if (subline) {
      ctx.font = Math.round(w * 0.038) + 'px "Work Sans", sans-serif';
      ctx.textAlign = opts.center ? 'center' : 'left';
      ctx.fillText(subline, opts.center ? x + w / 2 : x + pad, h * 0.78);
    }
  }

  function primaryPhoto() {
    return state.photos.length ? state.photos[0].img : null;
  }

  function layoutDimensions(layout) {
    if (layout.type === 'grid') {
      return {
        frameW: GRID_W,
        frameH: GRID_H,
        masterW: GRID_W * layout.cols,
        masterH: GRID_H * layout.rows,
      };
    }
    if (layout.type.indexOf('story') === 0) {
      return { frameW: STORY_W, frameH: STORY_H, masterW: STORY_W, masterH: STORY_H };
    }
    return {
      frameW: CAROUSEL_W,
      frameH: CAROUSEL_H,
      masterW: CAROUSEL_W * layout.frames,
      masterH: CAROUSEL_H,
    };
  }

  function renderMaster(layout, scale) {
    scale = scale || 1;
    var dim = layoutDimensions(layout);
    var canvas = document.createElement('canvas');
    canvas.width = Math.round(dim.masterW * scale);
    canvas.height = Math.round(dim.masterH * scale);
    var ctx = canvas.getContext('2d');
    var tok = tokens(state.style);
    var img = primaryPhoto();
    var fw = dim.frameW * scale;
    var fh = dim.frameH * scale;

    ctx.fillStyle = '#1A1A1A';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (layout.type === 'pano') {
      drawCoverImage(ctx, img, 0, 0, canvas.width, canvas.height, state.zoom, state.panX, state.panY);
    } else if (layout.type === 'grid') {
      drawCoverImage(ctx, img, 0, 0, canvas.width, canvas.height, state.zoom, state.panX, state.panY);
    } else if (layout.type === 'tpt') {
      drawTypeCard(ctx, 0, 0, fw, fh, state.style, tok, state.headline, state.subline, 0);
      drawCoverImage(ctx, img, fw, 0, fw, fh, state.zoom, state.panX, state.panY);
      drawTypeCard(ctx, fw * 2, 0, fw, fh, state.style, tok, COPY.cta, 'lankafreediving.com', 1, { center: true });
    } else if (layout.type === 'quote') {
      drawTypeCard(ctx, 0, 0, fw, fh, state.style, tok, COPY.kicker, state.subline, 0);
      drawCoverImage(ctx, img, fw, 0, fw, fh, state.zoom, state.panX, state.panY);
      drawTypeCard(ctx, fw * 2, 0, fw, fh, state.style, tok, COPY.quote.split('\n')[0], COPY.quote.split('\n')[1] || '', 2, { center: true });
      drawCoverImage(ctx, img, fw * 3, 0, fw, fh, state.zoom, state.panX, state.panY);
      drawTypeCard(ctx, fw * 4, 0, fw, fh, state.style, tok, COPY.cta, 'Link in bio', 3, { center: true });
    } else if (layout.type === 'story-photo') {
      drawCoverImage(ctx, img, 0, 0, canvas.width, canvas.height, state.zoom, state.panX, state.panY);
      var barH = canvas.height * 0.22;
      ctx.fillStyle = state.style === 'sleeve' ? '#D94F2A' : '#1A1A1A';
      ctx.fillRect(0, canvas.height - barH, canvas.width, barH);
      ctx.fillStyle = state.style === 'sleeve' ? '#F0C419' : '#F5EDE0';
      ctx.font = Math.round(canvas.width * 0.065) + 'px "Bowlby One SC", serif';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      wrapText(ctx, state.headline.toUpperCase(), canvas.width * 0.06, canvas.height - barH / 2 - canvas.width * 0.04, canvas.width * 0.88, canvas.width * 0.07);
    } else if (layout.type === 'story-type') {
      var pair = tok.pairs[0];
      ctx.fillStyle = pair.bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      if (state.style === 'quiet') drawQuietWave(ctx, 0, 0, canvas.width, canvas.height, pair.fg);
      drawTypeCard(ctx, 0, 0, canvas.width, canvas.height, state.style, tok, state.headline, state.subline, 0, { center: true });
    } else if (layout.type === 'story-logo') {
      var p2 = tok.pairs[state.style === 'sleeve' ? 0 : 1];
      ctx.fillStyle = p2.bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      if (state.logo) {
        var logoSize = canvas.width * 0.42;
        var lx = (canvas.width - logoSize) / 2;
        var ly = (canvas.height - logoSize) / 2;
        ctx.fillStyle = p2.fg;
        ctx.fillRect(lx - tok.border, ly - tok.border, logoSize + tok.border * 2, logoSize + tok.border * 2);
        ctx.drawImage(state.logo, lx, ly, logoSize, logoSize);
      }
      ctx.fillStyle = p2.fg;
      ctx.font = Math.round(canvas.width * 0.05) + 'px "Bowlby One SC", serif';
      ctx.textAlign = 'center';
      ctx.fillText(state.subline.toUpperCase(), canvas.width / 2, canvas.height * 0.82);
    }

    return { canvas: canvas, dim: dim };
  }

  function sliceFrames(masterCanvas, layout) {
    var dim = layoutDimensions(layout);
    var frames = [];
    var scale = masterCanvas.width / dim.masterW;

    if (layout.type === 'grid') {
      var uploadMeta = [];
      for (var v = 0; v < layout.frames; v++) {
        var col = v % layout.cols;
        var row = Math.floor(v / layout.cols);
        var uploadNum = layout.frames - v;
        uploadMeta.push({ visual: v, uploadNum: uploadNum, col: col, row: row });
      }
      uploadMeta.sort(function (a, b) { return a.uploadNum - b.uploadNum; });

      uploadMeta.forEach(function (meta) {
        var c = document.createElement('canvas');
        c.width = dim.frameW;
        c.height = dim.frameH;
        var ctx = c.getContext('2d');
        ctx.drawImage(
          masterCanvas,
          meta.col * dim.frameW * scale,
          meta.row * dim.frameH * scale,
          dim.frameW * scale,
          dim.frameH * scale,
          0, 0,
          dim.frameW,
          dim.frameH
        );
        frames.push({
          canvas: c,
          label: 'Post ' + String(meta.uploadNum).padStart(2, '0') + ' · upload ' + (meta.uploadNum === 1 ? 'first' : meta.uploadNum === layout.frames ? 'last' : ' #' + meta.uploadNum),
          filename: 'lanka-' + state.style + '-' + layout.id + '-' + String(meta.uploadNum).padStart(2, '0') + '.png',
        });
      });
    } else {
      for (var i = 0; i < layout.frames; i++) {
        var fc = document.createElement('canvas');
        fc.width = dim.frameW;
        fc.height = dim.frameH;
        var fctx = fc.getContext('2d');
        fctx.drawImage(
          masterCanvas,
          i * dim.frameW * scale,
          0,
          dim.frameW * scale,
          dim.frameH * scale,
          0, 0,
          dim.frameW,
          dim.frameH
        );
        frames.push({
          canvas: fc,
          label: 'Slide ' + String(i + 1).padStart(2, '0'),
          filename: 'lanka-' + state.style + '-' + layout.id + '-' + String(i + 1).padStart(2, '0') + '.png',
        });
      }
    }
    return frames;
  }

  function updatePreview() {
    if (!state.layout) return;
    var result = renderMaster(state.layout, 1);
    var master = result.canvas;
    var preview = els.previewCanvas;
    var maxW = Math.min(680, window.innerWidth - 32);
    var previewScale = maxW / master.width;
    preview.width = Math.round(master.width * previewScale);
    preview.height = Math.round(master.height * previewScale);
    var ctx = preview.getContext('2d');
    ctx.drawImage(master, 0, 0, preview.width, preview.height);
    updateGuides(previewScale);
  }

  function updateGuides(previewScale) {
    var overlay = els.guideOverlay;
    overlay.innerHTML = '';
    if (!state.showGuides || !state.layout) {
      overlay.hidden = true;
      return;
    }
    overlay.hidden = false;
    var layout = state.layout;
    var dim = layoutDimensions(layout);
    var preview = els.previewCanvas;

    if (layout.type === 'pano' || layout.type === 'tpt' || layout.type === 'quote') {
      for (var i = 1; i < layout.frames; i++) {
        var line = document.createElement('div');
        line.className = 'slice-line slice-line-v';
        line.style.left = (i * dim.frameW * previewScale) + 'px';
        overlay.appendChild(line);
      }
      if (layout.type === 'pano' || layout.frames >= 1) {
        var safeW = CAROUSEL_H * (3 / 4) * previewScale;
        var safeH = CAROUSEL_H * previewScale;
        var offsetX = (dim.frameW * previewScale - safeW) / 2;
        var zone = document.createElement('div');
        zone.className = 'safe-zone';
        zone.style.width = safeW + 'px';
        zone.style.height = safeH + 'px';
        zone.style.left = offsetX + 'px';
        zone.style.top = '0';
        zone.title = '3:4 grid thumbnail safe zone (first slide)';
        overlay.appendChild(zone);
      }
    }

    if (layout.type === 'grid') {
      for (var c = 1; c < layout.cols; c++) {
        var vLine = document.createElement('div');
        vLine.className = 'slice-line slice-line-v';
        vLine.style.left = (c * GRID_W * previewScale) + 'px';
        overlay.appendChild(vLine);
      }
      for (var r = 1; r < layout.rows; r++) {
        var hLine = document.createElement('div');
        hLine.className = 'slice-line slice-line-h';
        hLine.style.top = (r * GRID_H * previewScale) + 'px';
        overlay.appendChild(hLine);
      }
    }
  }

  function renderLayoutCard(layout) {
    var card = document.createElement('button');
    card.type = 'button';
    card.className = 'layout-card';
    card.dataset.layoutId = layout.id;

    var previewWrap = document.createElement('div');
    previewWrap.className = 'layout-card-preview';
    var mini = document.createElement('canvas');
    previewWrap.appendChild(mini);
    card.appendChild(previewWrap);

    var meta = document.createElement('div');
    meta.className = 'layout-card-meta';
    meta.innerHTML = '<span class="layout-card-name">' + layout.name + '</span><span class="layout-card-detail">' + layout.detail + '</span>';
    card.appendChild(meta);

    card.addEventListener('click', function () {
      openEditor(layout);
    });

    requestAnimationFrame(function () {
      try {
        var w = previewWrap.clientWidth || 160;
        var dim = layoutDimensions(layout);
        var scale = w / dim.masterW;
        var result = renderMaster(layout, scale);
        mini.width = w;
        mini.height = Math.round(w * (result.canvas.height / result.canvas.width));
        mini.getContext('2d').drawImage(result.canvas, 0, 0, mini.width, mini.height);
      } catch (e) { /* preview optional */ }
    });

    return card;
  }

  function populateMoodboard() {
    ['carousel', 'grid', 'story'].forEach(function (cat) {
      var container = $('grid-layouts');
      if (cat === 'carousel') container = $('carousel-layouts');
      if (cat === 'story') container = $('story-layouts');
      container.innerHTML = '';
      LAYOUTS[cat].forEach(function (layout) {
        container.appendChild(renderLayoutCard(layout));
      });
    });
  }

  function renderPhotoStrip() {
    var strip = els.photoStrip;
    strip.innerHTML = '';
    state.photos.forEach(function (photo) {
      var thumb = document.createElement('div');
      thumb.className = 'photo-thumb';
      var img = document.createElement('img');
      img.src = photo.url;
      img.alt = 'Uploaded photo';
      thumb.appendChild(img);
      var rm = document.createElement('button');
      rm.type = 'button';
      rm.setAttribute('aria-label', 'Remove photo');
      rm.textContent = '×';
      rm.addEventListener('click', function () {
        removePhoto(photo.id);
      });
      thumb.appendChild(rm);
      strip.appendChild(thumb);
    });
    populateMoodboard();
    if (state.layout) updatePreview();
  }

  function addPhotos(files) {
    state.photos = state.photos.filter(function (p) { return p.id !== 'placeholder'; });
    Array.from(files).forEach(function (file) {
      if (!file.type.startsWith('image/')) return;
      var url = URL.createObjectURL(file);
      loadImage(url).then(function (img) {
        var entry = { id: Date.now() + Math.random(), url: url, img: img, blob: file };
        state.photos.push(entry);
        dbPut('photos', { id: entry.id, blob: file });
        renderPhotoStrip();
      });
    });
  }

  function removePhoto(id) {
    var photo = state.photos.find(function (p) { return p.id === id; });
    if (photo) URL.revokeObjectURL(photo.url);
    state.photos = state.photos.filter(function (p) { return p.id !== id; });
    dbDelete('photos', id);
    renderPhotoStrip();
  }

  function restorePhotos() {
    return dbGetAll('photos').then(function (rows) {
      return Promise.all(rows.map(function (row) {
        return blobToDataUrl(row.blob).then(function (dataUrl) {
          return loadImage(dataUrl).then(function (img) {
            var url = dataUrl;
            state.photos.push({ id: row.id, url: url, img: img, blob: row.blob });
          });
        });
      }));
    }).then(function () {
      renderPhotoStrip();
    });
  }

  function restorePrefs() {
    return dbGetAll('prefs').then(function (rows) {
      rows.forEach(function (row) {
        if (row.key === 'style') setStyle(row.value, true);
      });
    });
  }

  function savePref(key, value) {
    dbPut('prefs', { key: key, value: value });
  }

  function setStyle(style, skipSave) {
    state.style = style;
    document.body.dataset.style = style;
    document.querySelectorAll('.style-btn').forEach(function (btn) {
      btn.classList.toggle('is-active', btn.dataset.style === style);
    });
    if (!skipSave) savePref('style', style);
    populateMoodboard();
    if (state.layout) updatePreview();
  }

  function showView(name) {
    ['moodboard', 'editor', 'export'].forEach(function (v) {
      $('view-' + v).hidden = v !== name;
    });
    els.backBtn.hidden = name === 'moodboard';
  }

  function openEditor(layout) {
    state.layout = layout;
    els.headlineInput.value = state.headline;
    els.sublineInput.value = state.subline;
    els.zoomSlider.value = state.zoom;
    els.panXSlider.value = state.panX;
    els.panYSlider.value = state.panY;
    els.guidesToggle.checked = state.showGuides;
    showView('editor');
    updatePreview();
  }

  function generateFrames() {
    var result = renderMaster(state.layout, 1);
    var frames = sliceFrames(result.canvas, state.layout);
    var strip = els.frameStrip;
    strip.innerHTML = '';

    var pending = frames.length;
    frames.forEach(function (frame) {
      frame.canvas.toBlob(function (blob) {
        var url = URL.createObjectURL(blob);
        var item = document.createElement('div');
        item.className = 'frame-item';
        var img = document.createElement('img');
        img.src = url;
        img.alt = frame.label;
        item.appendChild(img);
        var label = document.createElement('div');
        label.className = 'frame-label';
        label.innerHTML = '<span>' + frame.label + '</span><a href="' + url + '" download="' + frame.filename + '">Download</a>';
        item.appendChild(label);
        strip.appendChild(item);
        pending--;
        if (pending === 0) showView('export');
      }, 'image/png');
    });
  }

  function populateMemePack() {
    var gallery = $('meme-pack-gallery');
    if (!gallery) return;
    gallery.innerHTML = '';
    MEME_PACK.forEach(function (group) {
      var section = document.createElement('div');
      section.className = 'export-gallery-group';
      var title = document.createElement('h3');
      title.className = 'export-group-title';
      title.textContent = group.title;
      section.appendChild(title);
      var grid = document.createElement('div');
      grid.className = 'export-gallery-grid';
      group.items.forEach(function (item) {
        var src = EXPORT_BASE + item.file;
        var card = document.createElement('div');
        card.className = 'export-card';
        if (item.type === 'video') {
          var video = document.createElement('video');
          video.src = src;
          video.muted = true;
          video.loop = true;
          video.playsInline = true;
          video.autoplay = true;
          video.setAttribute('aria-label', item.label);
          card.appendChild(video);
        } else {
          var img = document.createElement('img');
          img.src = src;
          img.alt = item.label;
          img.loading = 'lazy';
          card.appendChild(img);
        }
        var meta = document.createElement('div');
        meta.className = 'export-card-meta';
        meta.innerHTML = '<span>' + item.label + '</span><a href="' + src + '" download="' + item.file + '">Save</a>';
        card.appendChild(meta);
        grid.appendChild(card);
      });
      section.appendChild(grid);
      gallery.appendChild(section);
    });
  }

  function bindEvents() {
    els.photoInput.addEventListener('change', function (e) {
      if (e.target.files.length) addPhotos(e.target.files);
      e.target.value = '';
    });

    document.querySelectorAll('.style-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setStyle(btn.dataset.style);
      });
    });

    els.backBtn.addEventListener('click', function () {
      if (!$('view-export').hidden) {
        showView('editor');
      } else {
        state.layout = null;
        showView('moodboard');
      }
    });

    els.headlineInput.addEventListener('input', function () {
      state.headline = els.headlineInput.value || COPY.headline;
      updatePreview();
    });
    els.sublineInput.addEventListener('input', function () {
      state.subline = els.sublineInput.value || COPY.subline;
      updatePreview();
    });
    els.zoomSlider.addEventListener('input', function () {
      state.zoom = Number(els.zoomSlider.value);
      updatePreview();
    });
    els.panXSlider.addEventListener('input', function () {
      state.panX = Number(els.panXSlider.value);
      updatePreview();
    });
    els.panYSlider.addEventListener('input', function () {
      state.panY = Number(els.panYSlider.value);
      updatePreview();
    });
    els.guidesToggle.addEventListener('change', function () {
      state.showGuides = els.guidesToggle.checked;
      updatePreview();
    });

    els.generateBtn.addEventListener('click', generateFrames);
    els.newExportBtn.addEventListener('click', function () {
      state.layout = null;
      showView('moodboard');
    });

    window.addEventListener('resize', function () {
      if (state.layout && !$('view-editor').hidden) updatePreview();
    });
  }

  function init() {
    els = {
      photoInput: $('photo-input'),
      photoStrip: $('photo-strip'),
      previewCanvas: $('preview-canvas'),
      guideOverlay: $('guide-overlay'),
      headlineInput: $('headline-input'),
      sublineInput: $('subline-input'),
      zoomSlider: $('zoom-slider'),
      panXSlider: $('pan-x-slider'),
      panYSlider: $('pan-y-slider'),
      guidesToggle: $('guides-toggle'),
      generateBtn: $('generate-btn'),
      frameStrip: $('frame-strip'),
      backBtn: $('back-btn'),
      newExportBtn: $('new-export-btn'),
    };

    bindEvents();

    Promise.all([
      loadImage(LOGO_SRC).then(function (img) { state.logo = img; }),
      restorePrefs(),
      restorePhotos(),
    ]).then(function () {
      if (!state.photos.length) {
        return loadImage(PLACEHOLDER).then(function (img) {
          state.photos.push({ id: 'placeholder', url: PLACEHOLDER, img: img, blob: null });
        });
      }
    }).then(function () {
      renderPhotoStrip();
      populateMoodboard();
      populateMemePack();
    }).catch(function () {
      populateMoodboard();
      populateMemePack();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
