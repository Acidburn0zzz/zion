/**
 * Copyright (C) 2008 Joao Paulo de Souza Medeiros
 * Copyright (C) 2009 Adriano Monteiro Marques
 *
 * Author(s): João Paulo de Souza Medeiros <ignotus21@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 */

#ifndef STATISTIC_H
#define STATISTIC_H

#include <math.h>
#include "clann.h"
#include "matrix.h"

/**
 *
 */
inline clann_type
statistic_mean(const clann_type *list,
               const unsigned int length);

/**
 *
 */
inline clann_type
statistic_mean_matrix(const struct matrix *m);

/**
 *
 */
inline clann_type
statistic_mean_matrix_row(const struct matrix *m,
                          const unsigned int row);

/**
 *
 */
inline clann_type
statistic_mean_matrix_col(const struct matrix *m,
                          const unsigned int col);

/**
 *
 */
inline clann_type
statistic_variance(const clann_type *list,
                   const clann_type *probability,
                   const unsigned int length);

/**
 *
 */
inline clann_type
statistic_variance_matrix(const struct matrix *m,
                          const clann_type *probability);

/**
 *
 */
inline clann_type
statistic_variance_matrix_row(const struct matrix *m,
                              const clann_type *probability,
                              const unsigned int row);

/**
 *
 */
inline clann_type
statistic_variance_matrix_col(const struct matrix *m,
                              const clann_type *probability,
                              const unsigned int col);

#endif
