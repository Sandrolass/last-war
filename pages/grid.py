import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧱MAP CREATOR")

# HTML completo que incluye CSS y JS embebido
html_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    @import url(https://fonts.googleapis.com/css?family=Frijole);
    @import url('https://fonts.googleapis.com/css?family=Pacifico');

    body {
      background: rgba(25, 100, 120, 0.5);
      font-family: sans-serif;
    }

    h1 {
      font-family: Pacifico;
      color: #FF3333;
      font-size: 2.5em;
      text-align: center;
      transition: all 0.5s;
      margin: 0px;
      padding: 0px;
    }

    h1:hover {
      animation: neon2 1.5s ease-in-out infinite alternate;
    }

    @keyframes neon2 {
      from {
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff,
                     0 0 40px #228DFF, 0 0 70px #228DFF,
                     0 0 80px #228DFF, 0 0 100px #228DFF, 0 0 150px #228DFF;
      }
      to {
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #fff,
                     0 0 20px #228DFF, 0 0 35px #228DFF,
                     0 0 40px #228DFF, 0 0 50px #228DFF, 0 0 75px #228DFF;
      }
    }

    #Contenedor {
      padding: 20px;
    }

    #contenedorCanvas {
      text-align: center;
    }

    canvas {
      background-color: #FFF;
      border: dotted 3px yellow;
      border-radius: 2px;
    }

    #herramientas {
      margin: 10px 60px 10px 60px;
      padding: 20px;
      border: 4px solid #FF4444;
      border-radius: 3px;
      color: #FF4444;
      background: #FFE94A;
    }

    #sizeCuadros {
      width: 42px;
    }

    .enlace {
      text-decoration: none;
      margin-left: 100px;
      font-size: 14pt;
      font-weight: bold;
    }

    .enlace:hover {
      color: red;
      text-shadow: 1px 1px 10px blue;
    }
  </style>
</head>
<body>
  <div id="Contenedor">
    <div id="contenedorCanvas">
      <canvas id="canvas1" width="1200" height="640">
        Tu navegador no soporta canvas
      </canvas>
    </div>
   <div id="herramientas">
  Color:
  <input type="color" id="color" value="#FF0000" onchange="cambiarColor()"/>

  Tamaño celda:
  <input type="number" id="sizeCuadros" value="10">

  Elemento:
  <select id="elemento">
  <option value="A">Base (3x3)</option>
  <option value="B">Alliance Center (9x9)</option>
  <option value="C">One By One (1x1)</option>
  <option value="D">Nuke (35x35)</option>
  <option value="eraser">🧽 Borrador (3x3)</option>
</select>

</div>
  </div>

  <script>
    window.onload = function() {
      var elementos = {
  "A": { ancho: 3, alto: 3 },
  "B": { ancho: 9, alto: 9 },
  "C": { ancho: 1, alto: 1 },
  "D": { ancho :35 , alto: 35 },
  "eraser": { ancho: 3, alto: 3 } // Puedes ajustar el tamaño del área a borrar
};

var selectorElemento = document.getElementById("elemento");
      var mouse = false;
      var canvas = document.getElementById("canvas1");
      var contenedor = document.getElementById("Contenedor");
      var cuadritos = [];
      var sizeCuadro = { ancho: 25, alto: 25 };
      var color = "";
      var inputColor = document.getElementById("color");
      var inputSizeCuadros = document.getElementById("sizeCuadros");
      console.log(inputSizeCuadros.value);

      if (canvas && canvas.getContext) {
        var ctx = canvas.getContext("2d");
        if (ctx) {
          function dibujaGrid(disX, disY, anchoLinea, color) {
            ctx.strokeStyle = color;
            ctx.lineWidth = anchoLinea;
            var columnas = [];
            var filas = [];
            for (let i = disX; i < canvas.width; i += disX) {
              ctx.beginPath();
              ctx.moveTo(i, 0);
              ctx.lineTo(i, canvas.height);
              ctx.stroke();
              columnas.push(i);
            }
            for (let i = disY; i < canvas.height; i += disY) {
              ctx.beginPath();
              ctx.moveTo(0, i);
              ctx.lineTo(ctx.canvas.width, i);
              ctx.stroke();
              filas.push(i);
            }
            columnas.push(0);
            filas.push(0);
            for (let x = 0; x < columnas.length; x++) {
              for (let y = 0; y < filas.length; y++) {
                cuadritos.push([columnas[x], filas[y], disX, disY]);
              }
            }
          }

          function fillCell(x, y) {
  let el = selectorElemento.value;
  let cellW = sizeCuadro.ancho;
  let cellH = sizeCuadro.alto;
  let anchoElement = elementos[el].ancho;
  let altoElement = elementos[el].alto;

  for (let i = 0; i < cuadritos.length; i++) {
    let cuadro = cuadritos[i];
    if (
      x > cuadro[0] &&
      x < cuadro[0] + cellW &&
      y > cuadro[1] &&
      y < cuadro[1] + cellH
    ) {
      if (el === "eraser") {
        ctx.clearRect(
          cuadro[0],
          cuadro[1],
          cellW * anchoElement,
          cellH * altoElement
        );
      } else {
        color = inputColor.value;
        ctx.fillStyle = color;
        ctx.fillRect(
          cuadro[0],
          cuadro[1],
          cellW * anchoElement,
          cellH * altoElement
        );
      }
      break;
    }
  }

  dibujaGrid(cellW, cellH, 0.4, "#44414B");
}


          canvas.onmousemove = function(e) {
            if (mouse) {
              var canvaspos = canvas.getBoundingClientRect();
              fillCell(e.clientX - canvaspos.left, e.clientY - canvaspos.top);
            }
          };

          canvas.onclick = function(e) {
            var canvaspos = canvas.getBoundingClientRect();
            fillCell(e.clientX - canvaspos.left, e.clientY - canvaspos.top);
          };

          canvas.onmousedown = function() {
            mouse = true;
          };

          canvas.onmouseup = function() {
            mouse = false;
          };

          inputSizeCuadros.addEventListener(
            "change",
            function() {
            console.log(this.value);
              cuadritos = [];
              sizeCuadro.ancho = parseInt(this.value);
              sizeCuadro.alto = parseInt(this.value);
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              dibujaGrid(sizeCuadro.ancho, sizeCuadro.alto, 1, "#44414B");
            },
            false
          );

          canvas.width = contenedor.offsetWidth - 400;
          dibujaGrid(sizeCuadro.ancho, sizeCuadro.alto, 1, "#44414B");
        } else {
          alert("No se pudo cargar el contexto");
        }
      }
    };
  </script>
</body>
</html>
"""

# Mostrar el HTML personalizado
components.html(html_code, height= 900 , scrolling=True)
