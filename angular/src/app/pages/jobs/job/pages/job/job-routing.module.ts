import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { JobComponent } from './job.component';
import { CodeComponent } from './code/code.component';
import { VarsComponent } from './vars/vars.component';
import { AuthGuard } from 'src/app/services/auth/AuthGuard ';

const routes: Routes = [
  {
    path: '',
    canActivate: [AuthGuard],
    component: JobComponent,
    children: [
      { path: '', redirectTo: 'code' },
      { path: 'code', canActivate: [AuthGuard], component: CodeComponent },
      { path: 'vars', canActivate: [AuthGuard], component: VarsComponent },
      { path: '**', redirectTo: '' },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class JobRoutingModule {}
