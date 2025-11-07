const items = document.querySelectorAll(".item");
const previa = document.getElementById("previa");

// const imagens = [
//   {nome: "Santos - SP", img: "santos.jpeg"},
//   {nome: "Rio de Janeiro - RJ", img: "saopaulo.jpg"},
//   {nome: "", img: "riodejaneiro.jpg"},
//   {nome: "Belo Horizonte - MG", img: "belohorizonte.jpg"},
//   {nome: "Curitiba - PR", img: "curitiba.jpg"},
// ];

items.forEach(e => {
  e.addEventListener("mouseenter", () => {
    let atributo = e.getAttribute("data-img");
    previa.src = atributo
  })
})