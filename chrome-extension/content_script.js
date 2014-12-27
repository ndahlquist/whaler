/**
 * Our CSS makes the merge buttons blue.
 */
function injectCSS() {
  var link = document.createElement('link');
  link.href = chrome.extension.getURL('css/whaler.css');
  link.rel = 'stylesheet';
  head = document.getElementsByTagName ('head')[0] || document.documentElement;
  head.insertBefore(link, head.lastChild);
}

function modifyDocument() {
  mergeButton = document.querySelector('.merge-branch-action');
  if (mergeButton != null) {
    // Add our CSS tag to paint the button blue.
    mergeButton.className = mergeButton.className.replace(/primary/g, 'whaler');
    // Modify the text
    mergeButton.innerHTML = mergeButton.innerHTML.replace(/Merge pull request/g, 'Squash merge')
  }

  form = document.querySelector('.merge-branch-form');
  if (form != null) {
    // Redirect the form to our server so that we can handle the merge.
    form.action = 'https://whaler-on-fleek.appspot.com/queue_merge';

    confirmMergeButton = form.querySelector('.button');
    // Add our CSS tag to paint the button blue.
    confirmMergeButton.className = confirmMergeButton.className.replace(/primary/g, 'whaler');
  }
}

function domNodeInsertedCallback() {
    console.log('DomNodeInsertedCallback()');

    // We must remove the event listener before modifyDocument() to prevent recursion.
    document.removeEventListener('DOMNodeInserted', domNodeInsertedCallback);
    modifyDocument();
    document.addEventListener('DOMNodeInserted', domNodeInsertedCallback);
}

injectCSS();
modifyDocument();

// GitHub dynamically modifies the merge form. We need to make sure we apply our modifications when it is updated.
// TODO: This is allegedly terrible for performance. What's a better way of doing this?
document.addEventListener('DOMNodeInserted', domNodeInsertedCallback);

