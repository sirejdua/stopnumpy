#lang rosette/safe

(require rosette/lib/angelic  ; provides `choose*`
         rosette/lib/match    ; provides `match`
         math/array           ; matrix support
         )
; Tell Rosette we really do want to use integers.
(current-bitwidth #f)

; Syntax for DSL
(struct transpose (arg) #:transparent)


; Interpreter for our DSL.
; We just recurse on the program's syntax using pattern matching.
(define (interpret p)
  (match p
    [(transpose a)  (array-axis-swap (interpret a) 0 1)]
    [_ p]))


; Create an unknown expression -- one that can evaluate to several
; possible values.
(define (??expr terminals)
  (define a (apply choose* terminals))
  (choose* (transpose a)
           a))


(define (make-int x)
  (define-symbolic* i integer?)
  i)

; Variables 
(define x (build-array #(2 2) make-int))


(define sketch
  (??expr (list x)))

(define prog
  (transpose x))

(define M
  (synthesize
    #:forall (list x)
    #:guarantee (assert (equal? (interpret sketch) (interpret prog)))))

M

; Substitute the bindings in M into the sketch to get back the
; synthesized program.
(evaluate sketch M)