import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StewardDashboard } from './steward-dashboard';

describe('StewardDashboard', () => {
  let component: StewardDashboard;
  let fixture: ComponentFixture<StewardDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StewardDashboard],
    }).compileComponents();

    fixture = TestBed.createComponent(StewardDashboard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
