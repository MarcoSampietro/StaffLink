import { Injectable, inject, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class StewardService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.backendUrl}/api/turni`;

  public turniDisponibili = signal<any[]>([]);

  // --- NUOVO METODO: Crea l'header con il token ---
  private getAuthOptions() {
    // Recupera il token salvato al login. 
    // NOTA: Se il tuo AuthService l'ha salvato con un nome diverso (es. 'token'), modificalo qui.
    const token = localStorage.getItem('access_token'); 
    
    return {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
    };
  }

  caricaTurni() {
    // 1. Peschiamo il token
    const token = localStorage.getItem('access_token');
    
    // 2. Lo stampiamo nella console per vedere se esiste davvero!
    console.log("🕵️ TOKEN RECUPERATO IN ANGULAR:", token ? "Esiste!" : "VUOTO!");

    // 3. Creiamo l'header forzatamente qui dentro
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    // 4. Facciamo la chiamata
    return this.http.get<any[]>(`${this.baseUrl}/disponibili`, { headers }).pipe(
      tap(dati => this.turniDisponibili.set(dati))
    );
  }

  accettaTurno(id_settore: number) {
    // Aggiungiamo le opzioni di autenticazione come terzo parametro
    return this.http.post(`${this.baseUrl}/${id_settore}/accetta`, {}, this.getAuthOptions()).pipe(
      tap(() => {
        alert("Turno accettato in attesa di conferma!");
      })
    );
  }
}