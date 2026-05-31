import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService } from '../../../core/services/admin.service';

@Component({
  selector: 'app-users-manager',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './users-manager.component.html'
})
export class UsersManagerComponent implements OnInit {
  public adminService = inject(AdminService);
  ngOnInit() { this.adminService.caricaUtenti().subscribe(); }
  promuovi(id: string) {
    if(confirm("Promuovere a Organizzatore?")) {
      this.adminService.modificaRuoloUtente(id, 'organizzatore').subscribe();
    }
  }
}
