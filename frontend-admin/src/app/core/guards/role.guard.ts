import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const roleGuard = (allowedRoles: string[]): CanActivateFn => {
  return () => {
    const authService = inject(AuthService);
    const router = inject(Router);
    const currentRole = authService.ruolo();

    if (authService.isAuthenticated() && currentRole && allowedRoles.includes(currentRole)) {
      return true;
    }
    return router.parseUrl('/login');
  };
};
