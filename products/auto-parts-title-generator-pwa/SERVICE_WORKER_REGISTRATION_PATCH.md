# Service Worker Registration Patch

Status: ready_for_next_commit
Date: 2026-06-14

`sw.js` exists, but direct `index.html` update hit a GitHub SHA conflict during fast commits.

Add this before `</script>` or before `</body>` in `index.html`:

```html
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('./sw.js').catch(function () {});
}
</script>
```

Also make sure the page has:

```html
<link rel="manifest" href="./manifest.json" />
```

This is required before Android install-flow testing.
