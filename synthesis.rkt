#lang rosette

(require rosette/lib/angelic  ; provides `choose*`
         rosette/lib/match    ; provides `match`
         math/array           ; matrix support
         (only-in python py-import py-method-call)
         ;python/config
         )
; Tell Rosette we really do want to use integers.
(current-bitwidth #f)

; Only needs to be done once
;(enable-cpyimport!)

(define y1 '((1 2) (3 4)))

; Import python module
(py-import "prog" as python-module)
(py-method-call python-module "transpose_py" y1)

; Syntax for DSL
(struct transpose (arg)        #:transparent)
(struct sum (arg)                #:transparent)
;(struct dot (arg1 arg2)          #:transparent)
(struct element* (arg1 arg2)     #:transparent)
(struct element+ (arg1 arg2)     #:transparent)
;(struct extend (arg1 arg2)       #:transparent)
(struct matmul (arg1 arg2)     #:transparent)
(struct slice-col (arg1 arg2)  #:transparent)
(struct eye-like (arg)           #:transparent)
(struct eye-like-squares (arg)   #:transparent)
(struct zeros-like (arg)         #:transparent)
(struct ones-like (arg)          #:transparent)



; Interpreter for our DSL.
; We just recurse on the program's syntax using pattern matching.

(define (index a i j) (list-ref (list-ref a i) j))
(define (elementwise a b op) (for/list ([i (interpret a)] [j (interpret b)]) (for/list ([a i] [b j]) (op a b))))
; TODO use lists instead of arrays?
(define (interpret p)
  (match p
    [(transpose a)         (apply map list (interpret a))]
    [(sum a)               (list (list (apply + (interpret a))))]
    [(element* a b)        (elementwise (interpret a) (interpret b) *)]
    [(element+ a b)        (elementwise (interpret a) (interpret b) +)]
    ;[(dot a b)             (sum (element* (interpret a) (interpret b)))]
    ;[(extend a b)          (array-list->array (list (interpret a) (interpret b)))]
    [(eye-like a)          (let ([a_ (interpret a)])
                             (build-list (length a_) (lambda (id) (build-list (length (car a_)) (lambda (id2) (if (equal? id id2) 1 0))))))]
    [(eye-like-squares a)  (let ([a_ (interpret a)])
                             (build-list (length a_) (lambda (id) (build-list (length a_)       (lambda (id2) (if (equal? id id2) 1 0))))))]
    [(zeros-like a)        (let ([a_ (interpret a)])
                             (build-list (length a_) (lambda (id) (build-list (length (car a_)) (lambda (id2) 0 )))))  ]
    [(ones-like a)         (let ([a_ (interpret a)])
                             (build-list (length a_) (lambda (id) (build-list (length (car a_)) (lambda (id2) 1 )))))  ]
    [(matmul a b)          (for/list ([i (interpret a)]) (for/list ([j (interpret (transpose b))]) (for/fold ([sum 0]) ([c i] [d j]) (+ sum (* c d)))))]
    [_ p]))


; Create an unknown expression -- one that can evaluate to several
; possible values.
(define (??expr terminals)
  (define a (apply choose* (??expr terminals) terminals))
  (define b (apply choose* (??expr terminals) terminals))
  (choose* (transpose a)
           (sum a)
           (element* a b)
           (element+ a b)
;           (dot a b)
;           (extend a b)
           (eye-like a)
           (eye-like-squares a)
           (zeros-like a)
           (ones-like a)
           (matmul a b)
           a))


(define (make-int x)
  (define-symbolic* i integer?)
  i)
(define (make-list n) 
  (build-list n (lambda (id) (build-list n (lambda (id2) (make-int n) )))))

; Variables 
(define x (make-list 2))
;(define y (make-list 2))
;(define z (make-list 2))
;(define a (make-int a))
;(define b (make-int b))
;(define c (make-int c))


(define sketch
  (??expr (list x)))

;(define prog
;  (py-method-call python-module "transpose_py" x))
(define prog
  (matmul (element+ (eye-like x) (ones-like x)) x ))

(define M
  (synthesize
    #:forall (list x)
    #:guarantee (assert (equal? (interpret sketch) prog))))

M

; Substitute the bindings in M into the sketch to get back the
; synthesized program.
;(evaluate sketch M)

;(interpret (matmul (eye-like x) x))
