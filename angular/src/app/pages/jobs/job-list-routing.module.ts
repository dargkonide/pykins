import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from 'src/app/services/auth/AuthGuard';

import { JobListComponent } from './job-list.component';

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], component: JobListComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class JobListRoutingModule {}
