var chatButton = document.querySelector('.chat-widget--button');
var chatBubble = document.querySelector('.chat-widget--bubble');

setTimeout(function() {
  chatBubble.classList.add('-hide');

chatButton.addEventListener('click', function() {
  void chatBubble.offsetWidth;
  chatBubble.classList.toggle('-hide');
}, false);
  }, 4000);