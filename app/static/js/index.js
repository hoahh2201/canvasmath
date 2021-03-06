function get_result() {
  $('#result').text('  Predicting...');
  var canvasObj = document.getElementById("canvas");
  var img = canvasObj.toDataURL('image/jpeg');
  $.ajax({
      type: "POST",
      url: $SCRIPT_ROOT + "/upload/",
      data: img,
      success: function(data) {
          $('#result').val(data);
          calc_result(data);
          recommend(data);
      }
  });
  console.log('mybtn');
  // console.log($('#result'));
  return $('#result');

}

function calc_result(calcu) {
  $('#result2').text('  Predicting...');
  $.ajax({
      type: "POST",
      url: $SCRIPT_ROOT + "/calcu/",
      data: calcu,
      success: function(data) {
          $('#result2').val(data);
      }
  });
  console.log('calcbtn');
  // console.log(calcu);

}

function recommend(calcu) {
  $.ajax({
      type: "POST",
      url: $SCRIPT_ROOT + "/get_type_math/",
      data: calcu,
      success: function(data) {
          appendText = '';
          data.split(';').forEach(e => {
              appendText += '<div class="col-10 embed-responsive embed-responsive-16by9" style="margin:50px auto">'
              appendText += '<iframe class="embed-responsive-item" src="' + e + '"></iframe>'
              appendText += '</div><br><br><br>'
          });;
          $('#recomendation').empty().append(appendText);
      }
  });
}
(function() {
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext("2d");

  canvas.width = $(window).width();
  canvas.height = 350;
  // 
  var Mouse = { x: 0, y: 0 };
  var lastMouse = { x: 0, y: 0 };
  // var background = new Image();
  // background.src = url('./static/img/background_canvas.jpg');
  // background.onload = function(){
  // 	context.drawImage(background,0,0);   
  // }

  context.fillStyle = "rgba(255,255,255,0.4)";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.color = "black";
  context.lineWidth = 1;
  context.lineJoin = context.lineCap = 'round';
  context.strokeStyle = "red";
  context.beginPath();
  for (var i = 130; i < 2500; i += 130) {
      for (var j = 0; j < 350; j += 5) {
          context.moveTo(i, j += 1);
          context.lineTo(i, j += 1);
      }
  }

  for (var t = 0; t < 2500; t += 5) {
      context.moveTo(t += 1, 150);
      context.lineTo(t += 1, 150);
  }
  context.closePath();
  context.stroke();
  debug();

  var history = {
      redo_list: [],
      undo_list: [],
      saveState: function(canvas, list, keep_redo) {
          keep_redo = keep_redo || false;
          if (!keep_redo) {
              this.redo_list = [];
          }
          this.undo_list.push(canvas.toDataURL());
      },
      undo: function(canvas, ctx) {
          this.restoreState(canvas, ctx, this.undo_list, this.redo_list);
      },

      restoreState: function(canvas, ctx, pop, push) {
          if (pop.length) {
              this.saveState(canvas, push, true);
              var restore_state = pop.pop();
              var img = document.createElement("img");
              img.setAttribute('src', pop[pop.length - 2]);
              this.undo_list.pop()
              img.setAttribute('alt', 'canvas');
              img.onload = function() {
                  ctx.clearRect(0, 0, canvas.width, 350);
                  console.log(canvas.width);
                  ctx.drawImage(img, 0, 0, canvas.width, 350, 0, 0, canvas.width, 350);
              }
          }
      }
  }

  canvas.addEventListener("mousemove", function(e) {
      lastMouse.x = Mouse.x;
      lastMouse.y = Mouse.y;

      Mouse.x = e.pageX - this.offsetLeft;
      Mouse.y = e.pageY - this.offsetTop;
      console.log(canvas.width);
  }, false);
  canvas.removeEventListener("mousemove", function(e) {
      //history.saveState(canvas, [], true)

      return $(this);
  }, false);

  canvas.addEventListener("mousedown", function(e) {
      canvas.addEventListener("mousemove", onPaint, false);
      //history.saveState(canvas, [], true)
  }, false);

  canvas.addEventListener("mouseup", function() {
      canvas.removeEventListener("mousemove", onPaint, false);
      history.saveState(canvas, [], true)

      get_result();

  }, false);
  $('#undo').on('click', function() {
      event.preventDefault();
      history.undo(canvas, context);
  });
  /* document.getElementById('undo').addEventListener('click', function () {
    pencil.init(canvas, context);
    history.undo(canvas, context);
  }); */




  var onPaint = function() {
      var c = document.getElementById("canvas");
      var context = c.getContext("2d");
      context.beginPath();
      context.lineWidth = context.lineWidth;
      context.lineJoin = "round";
      context.lineCap = "round";
      context.strokeStyle = context.color;

      context.beginPath();

      context.moveTo(lastMouse.x, lastMouse.y);


      context.lineTo(Mouse.x, Mouse.y);
      context.closePath();
      context.stroke();
  };

  function debug() {
      $("#clearButton").on("click", function() {
          // context.fillStyle = "rgba(255,255,255,0.4)";
          // context.clearRect(0, 0, canvas.width, canvas.height);
          // context.fillStyle="black"
          // context.fillRect(0, 0, canvas.width, canvas.height);
          // context.strokeStyle = "red";
          // context.beginPath();
          // for (var i=130; i<1800; i+=130 ){
          // 	for (var j=0; j<350; j+=5){
          // 		context.moveTo(i, j+=1);
          // 		context.lineTo(i, j+=1);
          // 	}
          // }

          // for (var t=0; t<1800; t+=5){
          // 	context.moveTo(t+=1,150);
          // 	context.lineTo(t+=1,150);
          // }
          // context.closePath();
          // context.stroke();
          var canvas = document.getElementById('canvas');
          var context = canvas.getContext("2d");

          canvas.width = $(window).width();
          canvas.height = 350;
          // 
          var Mouse = { x: 0, y: 0 };
          var lastMouse = { x: 0, y: 0 };
          // var background = new Image();
          // background.src = url('./static/img/background_canvas.jpg');
          // background.onload = function(){
          // 	context.drawImage(background,0,0);   
          // }

          context.fillStyle = "rgba(255,255,255,0.4)";
          context.fillRect(0, 0, canvas.width, canvas.height);
          context.color = "black";
          context.lineWidth = 1;
          context.lineJoin = context.lineCap = 'round';
          context.strokeStyle = "red";
          context.beginPath();
          for (var i = 130; i < 2100; i += 130) {
              for (var j = 0; j < 350; j += 5) {
                  context.moveTo(i, j += 1);
                  context.lineTo(i, j += 1);
              }
          }

          for (var t = 0; t < 2100; t += 5) {
              context.moveTo(t += 1, 150);
              context.lineTo(t += 1, 150);
          }
          context.closePath();
          context.stroke();
      });
  }


}()); 