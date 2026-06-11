/**
 * Funciones de utilidad para formatear datos
 */

// Formatear hora en formato HH:MM
export const formatHora = (horaStr) => {
  if (!horaStr) return '—'
  try {
    const hora = new Date(horaStr)
    return hora.toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit', hour12: false })
  } catch {
    return horaStr
  }
}

// Formatear fecha en formato DD/MM/YYYY
export const formatFecha = (fechaStr) => {
  if (!fechaStr) return '—'
  try {
    const fecha = new Date(fechaStr)
    return fecha.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })
  } catch {
    return fechaStr
  }
}

// Formatear horas trabajadas correctamente (evita mostrar 62 en lugar de 1h 2min)
export const formatHorasTrabajadas = (horas) => {
  if (horas === null || horas === undefined || horas === 0) return '—'
  
  // Si es un número decimal como 1.03, convertir a formato de horas y minutos
  if (typeof horas === 'number') {
    const horasEnteras = Math.floor(horas)
    const minutosDecimal = (horas - horasEnteras) * 60
    const minutosEnteros = Math.round(minutosDecimal)
    
    // Si es exactamente una hora sin minutos
    if (minutosEnteros === 0) {
      return `${horasEnteras}h`
    }
    
    // Si tiene minutos
    return `${horasEnteras}h ${minutosEnteros}min`
  }
  
  return horas.toString()
}

// Formatear horas a formato legible completo (ej: "8 horas 2 minutos")
export const formatHorasLegibles = (horas) => {
  if (horas === null || horas === undefined || horas === 0) return '0 horas'
  
  if (typeof horas === 'number') {
    const horasEnteras = Math.floor(horas)
    const minutosDecimal = (horas - horasEnteras) * 60
    const minutosEnteros = Math.floor(minutosDecimal)
    const segundosDecimal = (minutosDecimal - minutosEnteros) * 60
    const segundosEnteros = Math.round(segundosDecimal)
    
    const partes = []
    
    if (horasEnteras > 0) {
      partes.push(horasEnteras === 1 ? '1 hora' : `${horasEnteras} horas`)
    }
    
    if (minutosEnteros > 0) {
      partes.push(minutosEnteros === 1 ? '1 minuto' : `${minutosEnteros} minutos`)
    }
    
    if (segundosEnteros > 0 && partes.length < 3) {
      partes.push(segundosEnteros === 1 ? '1 segundo' : `${segundosEnteros} segundos`)
    }
    
    return partes.length > 0 ? partes.join(' ') : 'menos de 1 segundo'
  }
  
  return horas.toString()
}

// Formatear fecha completa con día de la semana
export const formatFechaCompleta = (fechaStr) => {
  if (!fechaStr) return '—'
  try {
    const fecha = new Date(fechaStr)
    return fecha.toLocaleDateString('es-BO', {
      weekday: 'long', 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric'
    })
  } catch {
    return fechaStr
  }
}

// Formatear fecha y hora juntos
export const formatFechaHora = (fechaStr) => {
  if (!fechaStr) return '—'
  try {
    const fecha = new Date(fechaStr)
    return fecha.toLocaleString('es-BO', {
      day: '2-digit',
      month: '2-digit', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    })
  } catch {
    return fechaStr
  }
}
