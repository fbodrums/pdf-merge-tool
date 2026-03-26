import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const alertVariants = cva(
  'relative flex w-full flex-col gap-2 rounded-lg border border-[hsl(var(--border))] px-4 py-3 text-sm',
  {
    variants: {
      variant: {
        default: 'bg-[hsl(var(--card))] text-[hsl(var(--card-foreground))]',
        destructive:
          'border-[hsl(var(--destructive))]/30 bg-[hsl(var(--card))] text-[hsl(var(--destructive))]',
        warning:
          'border-amber-500/40 bg-amber-500/5 text-[hsl(var(--foreground))] [&_[data-slot=alert-description]]:text-[hsl(var(--muted-foreground))]',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
)

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof alertVariants>
>(({ className, variant, ...props }, ref) => (
  <div
    ref={ref}
    role="alert"
    data-slot="alert"
    className={cn(alertVariants({ variant }), className)}
    {...props}
  />
))
Alert.displayName = 'Alert'

const AlertTitle = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      data-slot="alert-title"
      className={cn('font-semibold leading-none tracking-tight', className)}
      {...props}
    />
  ),
)
AlertTitle.displayName = 'AlertTitle'

const AlertDescription = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      data-slot="alert-description"
      className={cn('text-sm text-[hsl(var(--muted-foreground))]', className)}
      {...props}
    />
  ),
)
AlertDescription.displayName = 'AlertDescription'

export { Alert, AlertTitle, AlertDescription }
