import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html'
})
export class HomeComponent {
  eventiPubblici = [
    { titolo: 'Concerto Rock: The Legends', data: '15 Luglio 2026', posti: 'Sold Out' },
    { titolo: 'Finale Campionato Basket', data: '22 Luglio 2026', posti: 'Ultimi Biglietti' },
    { titolo: 'Spettacolo Teatrale: L\'Opera', data: '05 Agosto 2026', posti: 'Disponibile' }
  ];
}
