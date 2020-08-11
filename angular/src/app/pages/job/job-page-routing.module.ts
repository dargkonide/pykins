import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { BuildComponent } from './pages/build/build.component';
import { JobPageComponent } from './job-page.component';
import {JobService} from './service/job.service';

const routes: Routes = [{
  path: '', component: JobPageComponent,
  children: [
    { path: '', redirectTo: 'history' },

    {path: 'job', loadChildren: () => import('./pages/job/job.module').then(m => m.JobModule), canActivate: [JobService] },
    {path: 'build', component: BuildComponent},
    {path: 'history', loadChildren: () => import('./pages/history/history.module').then(m => m.HistoryModule) },

    { path: '**', redirectTo: '' },

  ]
 }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobRoutingModule { }
