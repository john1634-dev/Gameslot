(function () {
  function createPasteFile(blob, input) {
    const extension = blob.type === 'image/jpeg' ? 'jpg' : 'png';
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    return new File([blob], `${input.name || 'screenshot'}-${timestamp}.${extension}`, {
      type: blob.type || 'image/png',
    });
  }

  function setFile(input, file) {
    const transfer = new DataTransfer();
    transfer.items.add(file);
    input.files = transfer.files;
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function findImageBlob(event) {
    const items = event.clipboardData && Array.from(event.clipboardData.items || []);
    const imageItem = items.find((item) => item.type && item.type.indexOf('image/') === 0);
    return imageItem ? imageItem.getAsFile() : null;
  }

  function updatePreview(zone, file) {
    const preview = zone.querySelector('.screenshot-paste-preview');
    const status = zone.querySelector('.screenshot-paste-status');
    const imageUrl = URL.createObjectURL(file);
    preview.innerHTML = `<img src="${imageUrl}" alt="Pasted screenshot preview">`;
    status.textContent = `${file.name} is ready to upload. Save this form to keep it.`;
    zone.classList.add('has-image');
  }

  function buildZone(input) {
    const zone = document.createElement('div');
    zone.className = 'screenshot-paste-zone';
    zone.tabIndex = 0;
    zone.setAttribute('role', 'button');
    zone.setAttribute('aria-label', 'Paste screenshot image');
    zone.innerHTML = [
      '<strong>Paste screenshot</strong>',
      '<span>Click here, then press Ctrl+V to fill this image field.</span>',
      '<small class="screenshot-paste-status">PNG and JPG clipboard images are supported.</small>',
      '<div class="screenshot-paste-preview" aria-hidden="true"></div>',
    ].join('');

    zone.addEventListener('click', function () {
      zone.focus();
    });

    zone.addEventListener('paste', function (event) {
      const blob = findImageBlob(event);
      const status = zone.querySelector('.screenshot-paste-status');

      if (!blob) {
        status.textContent = 'No image was found in the clipboard.';
        zone.classList.add('has-error');
        return;
      }

      event.preventDefault();
      zone.classList.remove('has-error');
      const file = createPasteFile(blob, input);
      setFile(input, file);
      updatePreview(zone, file);
    });

    return zone;
  }

  function enhanceImageInput(input) {
    if (input.dataset.screenshotPasteReady === 'true') {
      return;
    }

    input.dataset.screenshotPasteReady = 'true';
    const row = input.closest('.form-row, .field-cover_image, .el-form-item, p, div') || input.parentElement;
    const zone = buildZone(input);
    row.appendChild(zone);
  }

  function initScreenshotPaste() {
    document
      .querySelectorAll('input[type="file"][name$="cover_image"], input[type="file"][accept*="image"]')
      .forEach(enhanceImageInput);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScreenshotPaste);
  } else {
    initScreenshotPaste();
  }
})();
