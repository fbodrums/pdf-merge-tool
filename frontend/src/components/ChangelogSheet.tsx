import { useMemo } from 'react'
import type { ComponentProps } from 'react'
import ReactMarkdown from 'react-markdown'
import type { Components } from 'react-markdown'
import remarkGfm from 'remark-gfm'

import { Button } from '@/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet'
import { cn } from '@/lib/utils'

import changelogSource from '../../../CHANGELOG.md?raw'

const mdBase = 'text-[hsl(var(--foreground))]'

export function ChangelogSheet() {
  const components: Components = useMemo(
    () => ({
      h1: ({ className, ...props }: ComponentProps<'h1'>) => (
        <h1 className={cn('text-xl font-semibold tracking-tight', mdBase, className)} {...props} />
      ),
      h2: ({ className, ...props }: ComponentProps<'h2'>) => (
        <h2 className={cn('mt-6 text-lg font-semibold first:mt-0', mdBase, className)} {...props} />
      ),
      h3: ({ className, ...props }: ComponentProps<'h3'>) => (
        <h3 className={cn('mt-4 text-base font-medium', mdBase, className)} {...props} />
      ),
      p: ({ className, ...props }: ComponentProps<'p'>) => (
        <p className={cn('text-[hsl(var(--muted-foreground))]', className)} {...props} />
      ),
      ul: ({ className, ...props }: ComponentProps<'ul'>) => (
        <ul className={cn('list-disc space-y-1 pl-5 text-[hsl(var(--muted-foreground))]', className)} {...props} />
      ),
      ol: ({ className, ...props }: ComponentProps<'ol'>) => (
        <ol className={cn('list-decimal space-y-1 pl-5 text-[hsl(var(--muted-foreground))]', className)} {...props} />
      ),
      li: ({ className, ...props }: ComponentProps<'li'>) => (
        <li className={cn('leading-relaxed', className)} {...props} />
      ),
      a: ({ className, ...props }: ComponentProps<'a'>) => (
        <a
          className={cn('font-medium text-[hsl(var(--primary))] underline underline-offset-4 hover:opacity-90', className)}
          target="_blank"
          rel="noreferrer noopener"
          {...props}
        />
      ),
      img: ({ className, alt, ...props }: ComponentProps<'img'>) => (
        <img className={cn('h-auto max-w-full', className)} alt={alt ?? ''} {...props} />
      ),
      code: ({ className, ...props }: ComponentProps<'code'>) => (
        <code
          className={cn(
            'rounded bg-[hsl(var(--muted))] px-1.5 py-0.5 font-mono text-[0.9em] text-[hsl(var(--foreground))]',
            className,
          )}
          {...props}
        />
      ),
      hr: ({ className, ...props }: ComponentProps<'hr'>) => (
        <hr className={cn('my-6 border-[hsl(var(--border))]', className)} {...props} />
      ),
    }),
    [],
  )

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button type="button" variant="outline" size="sm">
          Changelog
        </Button>
      </SheetTrigger>
      <SheetContent
        side="right"
        className="flex h-full max-h-screen w-full flex-col gap-0 overflow-hidden p-0 sm:max-w-lg"
      >
        <SheetHeader className="shrink-0 space-y-1 border-b border-[hsl(var(--border))] px-6 pb-4 pt-6 text-left">
          <SheetTitle>Changelog</SheetTitle>
          <SheetDescription className="sr-only">Histórico de versões e novidades do produto.</SheetDescription>
        </SheetHeader>
        <div className="min-h-0 flex-1 overflow-y-auto px-6 py-4">
          <div className="space-y-4 text-sm leading-relaxed">
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
              {changelogSource}
            </ReactMarkdown>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  )
}
