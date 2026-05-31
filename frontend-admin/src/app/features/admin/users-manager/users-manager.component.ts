import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService } from '../../../core/services/admin.service';

@Component({
  selector: 'app-users-manager',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 20px;">
      <h1>Gestione Personale</h1>
      <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <tr style="border-bottom: 2px solid #ddd; text-align: left;">
          <th>Cognome</th>
          <th>Nome</th>
          <th>Email</th>
          <th>Ruolo</th>
          <th>Azioni</th>
        </tr>
        @for (utente of adminService.utenti(); track utente.id_utente) {
          <tr style="border-bottom: 1px solid #ddd;">
            <td style="padding: 10px;"><strong>{{ utente.cognome }}</strong></td>
            <td>{{ utente.nome }}</td>
            <td>{{ utente.email }}</td>
            <td><b>{{ utente.ruolo }}</b></td>
            <td>
              @if (utente.ruolo === 'steward') {
                <button (click)="promuovi(utente.id_utente)" style="padding: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
                  Promuovi a Org.
                </button>
              }
            </td>
          </tr>
        }
      </table>
    </div>
  `
})
export class UsersManagerComponent implements OnInit {
  public adminService = inject(AdminService);
  
  ngOnInit() { 
    this.adminService.caricaUtenti().subscribe(); 
  }
  
  promuovi(id: string) {
    if(confirm("Sei sicuro di voler promuovere questo utente a Organizzatore?")) {
      this.adminService.modificaRuoloUtente(id, 'organizzatore').subscribe();
    }
  }
}