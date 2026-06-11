// Test directo para verificar si el endpoint responde
fetch('http://127.0.0.1:8000/api/v1/asistencias/publico/entrada', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'test' // username de prueba
  })
})
.then(response => {
  console.log('Status:', response.status);
  console.log('Headers:', response.headers);
  return response.json();
})
.then(data => console.log('Respuesta:', data))
.catch(error => console.error('Error completo:', error));
