import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from 'src/app/services/auth/AuthGuard';

import { HostsComponent } from './hosts.component';

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], component: HostsComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class HostsRoutingModule {}
