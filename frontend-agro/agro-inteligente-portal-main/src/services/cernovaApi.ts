// src/services/cernovaApi.ts
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const cernovaApi = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Medicina endpoints
export const medicinaService = {
  getConsultorios: () => cernovaApi.get('/medicina/consultorios'),
  createConsultorio: (data: any) => cernovaApi.post('/medicina/consultorios', data),
  
  getMedicos: (consultorioId?: string) => 
    cernovaApi.get('/medicina/medicos', { params: { consultorio_id: consultorioId } }),
  createMedico: (data: any) => cernovaApi.post('/medicina/medicos', data),
  
  getPacientes: (consultorioId?: string) => 
    cernovaApi.get('/medicina/pacientes', { params: { consultorio_id: consultorioId } }),
  createPaciente: (data: any) => cernovaApi.post('/medicina/pacientes', data),
  
  health: () => cernovaApi.get('/health'),
};
