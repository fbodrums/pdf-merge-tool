/**
 * Copyright (C) 2026 Fabio Rafael Belliny
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

import { cn } from '@/lib/utils'
import {
  WIZARD_STEPS,
  WIZARD_STEP_LABELS,
  type WizardStep,
  wizardStepIndex,
} from '@/lib/wizardSteps'

type WizardStepperProps = {
  currentStep: WizardStep
  className?: string
}

export function WizardStepper({ currentStep, className }: WizardStepperProps) {
  const active = wizardStepIndex(currentStep)

  return (
    <nav aria-label="Etapas do assistente" className={cn('w-full', className)}>
      <ol className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center sm:justify-between sm:gap-2">
        {WIZARD_STEPS.map((step, i) => {
          const done = i < active
          const current = i === active
          return (
            <li key={step} className="flex min-w-0 flex-1 items-center gap-2 sm:min-w-[5rem]">
              <span
                className={cn(
                  'flex h-8 w-8 shrink-0 items-center justify-center rounded-full border text-xs font-semibold',
                  current &&
                    'border-[hsl(var(--primary))] bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]',
                  done && 'border-[hsl(var(--primary))] bg-[hsl(var(--primary))]/15 text-[hsl(var(--primary))]',
                  !current &&
                    !done &&
                    'border-[hsl(var(--border))] bg-[hsl(var(--muted))]/50 text-[hsl(var(--muted-foreground))]',
                )}
                aria-current={current ? 'step' : undefined}
              >
                {i + 1}
              </span>
              <span
                className={cn(
                  'truncate text-sm font-medium',
                  current ? 'text-[hsl(var(--foreground))]' : 'text-[hsl(var(--muted-foreground))]',
                )}
              >
                {WIZARD_STEP_LABELS[step]}
              </span>
            </li>
          )
        })}
      </ol>
    </nav>
  )
}
