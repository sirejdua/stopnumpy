#lang rosette/safe

(require rosette/lib/angelic  ; provides `choose*`
         rosette/lib/match    ; provides `match`
         math/matrix           ; matrix support
         )
; Tell Rosette we really do want to use integers.
(current-bitwidth #f)

; Syntax for DSL
(struct transpose (arg) #:transparent)
(struct dot (arg1 arg2) #:transparent)


; Interpreter for our DSL.
; We just recurse on the program's syntax using pattern matching.
(define (interpret p)
  (match p
    [(transpose a)  (matrix-transpose (interpret a))]
    [(dot a b) (matrix-dot (interpret a) (interpret b))]
    [_ p]))


; Create an unknown expression -- one that can evaluate to several
; possible values.
(define (??expr terminals)
  (define a (apply choose* terminals))
  (define b (apply choose* terminals))
  (choose* (dot a b)
           (transpose a)
           a))


(define (make-int x y)
  (define-symbolic* i integer?)
  i)

; Variables 
(define x (build-matrix 2 1 make-int))


(define sketch
  (??expr (list x)))

(define prog
  (dot x x))

(define M
  (synthesize
    #:forall (list x)
    #:guarantee (assert (equal? (interpret sketch) (interpret prog)))))

M

; Substitute the bindings in M into the sketch to get back the
; synthesized program.
(evaluate sketch M)