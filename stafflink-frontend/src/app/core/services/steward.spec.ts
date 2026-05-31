import { TestBed } from '@angular/core/testing';

import { Steward } from './steward';

describe('Steward', () => {
  let service: Steward;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Steward);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
