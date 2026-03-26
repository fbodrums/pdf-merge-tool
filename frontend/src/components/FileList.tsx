import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  type DragEndEvent,
  useSensor,
  useSensors,
} from '@dnd-kit/core'
import {
  SortableContext,
  arrayMove,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { GripVertical, Trash2 } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { PageConfigInput } from '@/components/PageConfigInput'
import { Separator } from '@/components/ui/separator'
import { isPageSpecValid } from '@/lib/pageSpec'
import { cn } from '@/lib/utils'

export type FileRow = {
  file_id: string
  filename: string
  total_pages: number | null
  password_protected: boolean
  pages: string
}

type SortableRowProps = {
  row: FileRow
  onPagesChange: (id: string, pages: string) => void
  onRemove: (id: string) => void
  disabled?: boolean
}

function SortableItem({ row, onPagesChange, onRemove, disabled }: SortableRowProps) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: row.file_id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  return (
    <Card
      ref={setNodeRef}
      style={style}
      className={cn('p-4', isDragging && 'opacity-70 shadow-lg')}
    >
      <CardContent className="flex flex-col gap-3 p-0 sm:flex-row sm:items-start">
        <button
          type="button"
          className="mt-1 shrink-0 cursor-grab text-[hsl(var(--muted-foreground))] active:cursor-grabbing"
          {...attributes}
          {...listeners}
          aria-label="Reordenar"
        >
          <GripVertical className="h-5 w-5" />
        </button>
        <div className="min-w-0 flex-1 space-y-2">
          <div className="flex flex-wrap items-baseline gap-2">
            <p className="truncate font-medium">{row.filename}</p>
            <span className="text-xs text-[hsl(var(--muted-foreground))]">
              {row.password_protected
                ? 'Protegido por senha'
                : row.total_pages != null
                  ? `${row.total_pages} página(s)`
                  : '—'}
            </span>
          </div>
          <PageConfigInput
            id={`pages-${row.file_id}`}
            value={row.pages}
            onChange={(v) => onPagesChange(row.file_id, v)}
            disabled={disabled || row.password_protected}
          />
        </div>
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="shrink-0 text-[hsl(var(--destructive))]"
          onClick={() => onRemove(row.file_id)}
          disabled={disabled}
          aria-label="Remover"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </CardContent>
    </Card>
  )
}

type Props = {
  rows: FileRow[]
  onReorder: (rows: FileRow[]) => void
  onPagesChange: (id: string, pages: string) => void
  onRemove: (id: string) => void
  disabled?: boolean
}

export function FileList({ rows, onReorder, onPagesChange, onRemove, disabled }: Props) {
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 6 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
  )

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    if (!over || active.id === over.id) return
    const oldIndex = rows.findIndex((r) => r.file_id === active.id)
    const newIndex = rows.findIndex((r) => r.file_id === over.id)
    if (oldIndex < 0 || newIndex < 0) return
    onReorder(arrayMove(rows, oldIndex, newIndex))
  }

  const allSpecsValid = rows.every((r) => isPageSpecValid(r.pages))

  return (
    <Card>
      <CardHeader>
        <CardTitle>Arquivos e páginas</CardTitle>
        <p className="text-sm text-[hsl(var(--muted-foreground))]">
          Arraste pelo ícone à esquerda para alterar a ordem do merge.
          {!allSpecsValid && (
            <span className="ml-1 font-medium text-[hsl(var(--destructive))]">
              Corrija a sintaxe das páginas antes de gerar.
            </span>
          )}
        </p>
      </CardHeader>
      <CardContent>
        <DndContext
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <SortableContext items={rows.map((r) => r.file_id)} strategy={verticalListSortingStrategy}>
            <ul className="space-y-0">
              {rows.map((row, index) => (
                <li key={row.file_id}>
                  {index > 0 && <Separator className="my-3" />}
                  <SortableItem
                    row={row}
                    onPagesChange={onPagesChange}
                    onRemove={onRemove}
                    disabled={disabled}
                  />
                </li>
              ))}
            </ul>
          </SortableContext>
        </DndContext>
      </CardContent>
    </Card>
  )
}
