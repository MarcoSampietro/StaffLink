import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environments';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private http = inject(HttpClient);
  
  // Link corretto al cloud
  private baseUrl = `${environment.backendUrl}/api/admin`;

  public utenti = signal<any[]>([]);

  caricaUtenti() {
    return this.http.get<any[]>(`${this.baseUrl}/utenti`).pipe(
      tap(dati => this.utenti.set(dati))
    );
  }

  modificaRuoloUtente(id_utente: string, nuovo_ruolo: string) {
    return this.http.put(`${this.baseUrl}/utenti/${id_utente}/ruolo`, { ruolo: nuovo_ruolo }).pipe(
      tap(() => {
        this.caricaUtenti().subscribe();
      })
    );
  }
}