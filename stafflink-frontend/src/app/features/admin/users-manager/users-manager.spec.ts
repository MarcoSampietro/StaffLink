import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsersManager } from './users-manager';

describe('UsersManager', () => {
  let component: UsersManager;
  let fixture: ComponentFixture<UsersManager>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UsersManager],
    }).compileComponents();

    fixture = TestBed.createComponent(UsersManager);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
