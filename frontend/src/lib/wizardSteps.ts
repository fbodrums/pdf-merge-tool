/**
 * Copyright (C) 2026 Fabio Rafael Belliny
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

export const WIZARD_STEPS = ['select', 'uploading', 'configure', 'result'] as const

export type WizardStep = (typeof WIZARD_STEPS)[number]

export const WIZARD_STEP_LABELS: Record<WizardStep, string> = {
  select: 'Arquivos',
  uploading: 'Envio',
  configure: 'Configuração',
  result: 'Download',
}

export function wizardStepIndex(step: WizardStep): number {
  return WIZARD_STEPS.indexOf(step)
}
