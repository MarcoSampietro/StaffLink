import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class StewardService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.backendUrl}/api/turni`;

  public turniDisponibili = signal<any[]>([]);

  caricaTurni() {
    return this.http.get<any[]>(`${this.baseUrl}/disponibili`).pipe(
      tap(dati => this.turniDisponibili.set(dati))
    );
  }
}
