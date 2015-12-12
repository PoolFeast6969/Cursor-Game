function setupPointerLock() {
  document.addEventListener("mousemove", unlockCallback, false);
  document.addEventListener("click", clickCallback, false);
  document.addEventListener('pointerlockchange', changeCallback, false);
  document.addEventListener('mozpointerlockchange', changeCallback, false);
  document.addEventListener('webkitpointerlockchange', changeCallback, false);
};

function changeCallback(e) {
  var canvas = $("body").get()[0];
  if (document.pointerLockElement === canvas || document.mozPointerLockElement === canvas || document.webkitPointerLockElement === canvas) {
    cursoroffset.x = cursorX;
    cursoroffset.y = cursorY;
    document.removeEventListener("mousemove", unlockCallback, false);
    document.removeEventListener("click", clickCallback, false);
    document.addEventListener("mousemove", lockCallback, false);
  } else {
    document.removeEventListener("mousemove", lockCallback, false);
    document.addEventListener("mousemove", unlockCallback, false);
    document.addEventListener("click", clickCallback, false);
  }
};

function lockCallback(e) {
  var movementX = e.movementX || e.mozMovementX || e.webkitMovementX || 0;
  var movementY = e.movementY || e.mozMovementY || e.webkitMovementY || 0;
  coordinates.x = cursoroffset.x + movementX;
  coordinates.y = cursoroffset.y + movementY;
  cursoroffset.x = coordinates.x;
  cursoroffset.y = coordinates.y;
};

function unlockCallback(e) {
  coordinates.x = e.pageX;
  coordinates.y = e.pageY;
};

function clickCallback(e) {
  cursorX = e.pageX;
  cursorY = e.pageY;
  var canvas = $("body").get()[0];
  canvas.requestPointerLock = canvas.requestPointerLock || canvas.mozRequestPointerLock || canvas.webkitRequestPointerLock;
  canvas.requestPointerLock();
};

function connect(endpoint,authtoken) {
  var transport = WebSocket;
  var endpoint = endpoint;
  var options = {
    ignoreSender: false,
    authToken: authtoken
  };
  var connection = new Omnibus(transport, endpoint, options);
  var channel = connection.openChannel('mousemoves');

  connection
    .on(Omnibus.events.CONNECTION_CONNECTED, function(event) {
      console.log('Connected');
    })
    .on(Omnibus.events.CONNECTION_AUTHENTICATED, function(event) {
      console.log('Authenticated');
    });
  channel
    .on(Omnibus.events.CHANNEL_SUBSCRIBED, function(event) {
      console.log('Listening');
    })
    .on('move', function(event) {
      game[event.data.sender].move(event.data.payload.top, event.data.payload.left);
    })
    .on('update', function(event) {
      var servergame = event.data.payload;
      console.log('Recieved Game Object: '+JSON.stringify(servergame));
      console.log('Game Did Contain: '+JSON.stringify(game));
      var add = $(Object.keys(servergame)).not(Object.keys(game)).get();
      $.each(add, function(index, id) {
        game[id] = new player(servergame[id]['username'], servergame[id]['picture']);
      });
      var remove = $(Object.keys(game)).not(Object.keys(servergame)).get();
      $.each(remove, function(index, id) {
        game[id]['html'].remove();
        game[id] = null;
        delete game[id];
      });
      console.log('Game Now Contains: '+JSON.stringify(game));
    })
    .on('chat', function(event) {
      if (typeof game[event.data.sender] != "undefined") {
        var sender = game[event.data.sender]['username'];
      } else {
        var sender = event.data.sender;
      }
      message = sender+': '+event.data.payload['message'];
      $('.chatbox').append($('#chatline').html().format(message));
    });
  $('body').mousemove(function(e) {
    channel.send('move', {
      top: coordinates.y / $('body').height() * 100 + '%',
      left: coordinates.x / $('body').width() * 100 + '%'
    });
  });
  $( document ).ready(function() {
    $('input').bind("enterKey",function() {
      channel.send('chat', {
        message: this.value
      });
      this.value = null;
    });
    $('input').keydown(function(e) {
        if(e.keyCode == 13) {
            $(this).trigger("enterKey");
        }
    });
  });
};
