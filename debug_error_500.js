// Script para diagnosticar error 500 en registro de asistencia
// Ejecutar en la consola del navegador

async function debugError500() {
    console.log('🔍 Diagnosticando error 500 en registro de asistencia...');
    
    // 1. Obtener token
    const token = localStorage.getItem('token');
    if (!token) {
        console.error('❌ No hay token. Inicia sesión primero.');
        return;
    }
    
    console.log('✅ Token encontrado');
    
    // 2. Obtener perfil del usuario
    try {
        const perfilResponse = await fetch('http://127.0.0.1:8000/api/v1/usuarios/perfil', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!perfilResponse.ok) {
            console.error('❌ Error obteniendo perfil:', perfilResponse.status);
            return;
        }
        
        const perfil = await perfilResponse.json();
        console.log('✅ Perfil obtenido:', perfil);
        console.log('👤 Username:', perfil.username);
        console.log('📧 Email:', perfil.email);
        console.log('🎓 Rol:', perfil.rol?.nombre);
        
        // 3. Intentar registrar entrada con diagnóstico
        console.log('🧪 Intentando registrar entrada...');
        
        const entradaResponse = await fetch('http://127.0.0.1:8000/api/v1/asistencias/publico/entrada', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: perfil.username
            })
        });
        
        console.log('📊 Status:', entradaResponse.status);
        console.log('📋 Headers:', Object.fromEntries(entradaResponse.headers.entries()));
        
        if (entradaResponse.ok) {
            const data = await entradaResponse.json();
            console.log('✅ Entrada registrada:', data);
        } else {
            const errorText = await entradaResponse.text();
            console.error('❌ Error en entrada:');
            console.error('Status:', entradaResponse.status);
            console.error('Response:', errorText);
            
            // Intentar parsear como JSON
            try {
                const errorJson = JSON.parse(errorText);
                console.error('Error JSON:', errorJson);
            } catch (e) {
                console.error('Error no es JSON:', errorText);
            }
        }
        
    } catch (error) {
        console.error('❌ Error general:', error);
    }
}

// Función para probar si el backend está funcionando
async function testBackendHealth() {
    console.log('🏥 Verificando salud del backend...');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/docs');
        if (response.ok) {
            console.log('✅ Backend está funcionando');
        } else {
            console.error('❌ Backend no responde:', response.status);
        }
    } catch (error) {
        console.error('❌ Error conectando con backend:', error);
    }
}

// Función para verificar API base
async function testAPIBase() {
    console.log('🔍 Verificando API base...');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/');
        console.log('📊 Status:', response.status);
        
        if (response.ok) {
            console.log('✅ API base funciona');
        } else {
            console.error('❌ API base no funciona:', response.status);
        }
    } catch (error) {
        console.error('❌ Error en API base:', error);
    }
}

// Ejecutar diagnóstico completo
async function runFullDiagnosis() {
    console.log('🚀 Iniciando diagnóstico completo...');
    
    await testBackendHealth();
    await testAPIBase();
    await debugError500();
    
    console.log('📋 Diagnóstico completado. Revisa la consola del backend para más detalles.');
}

// Exportar funciones
window.debugError500 = {
    runFullDiagnosis,
    debugError500,
    testBackendHealth,
    testAPIBase
};

console.log('🔧 Herramientas de diagnóstico cargadas. Usa:');
console.log('  window.debugError500.runFullDiagnosis()');
console.log('  window.debugError500.debugError500()');
console.log('  window.debugError500.testBackendHealth()');
