import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { JobService } from './service/job.service';

import { BuildComponent } from './pages/build/build.component';
import { JobPageComponent } from './job-page.component';

const routes: Routes = [
  {
    path: '',
    component: JobPageComponent,
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'history' },

      {
        path: 'job',
        loadChildren: () =>
          import('./pages/job/job.module').then((m) => m.JobModule),
        canActivate: [JobService],
      },
      { path: 'build', component: BuildComponent },
      {
        path: 'history',
        loadChildren: () =>
          import('./pages/history/history-list/history-list.module').then(
            (m) => m.HistoryListModule
          ),
      },
      {
        path: 'history/:runId',
        loadChildren: () =>
          import('./pages/history/job-history/job-history.module').then(
            (m) => m.JobHistoryModule
          ),
      },

      { path: '**', redirectTo: 'history' },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class JobRoutingModule {}
